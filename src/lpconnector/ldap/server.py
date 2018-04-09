from __future__ import print_function
import sys
import ldap
from .objects import LDAPUser, LDAPGroup, LDAPObjectException


class LDAPServer(object):

    def __init__(self, **kwargs):
        config = dict(kwargs.get('config'))
        self.host = config.get('server')
        self.base_dn = config.get('base_dn')
        self.user = config.get('binding_user_uid')
        self.pwd = config.get('binding_user_pwd')
        self.ldap_server = None

    def bind_server(self):
        self.ldap_server = ldap.initialize(self.host)   # pylint: disable=no-member

        bind_dn = "uid=" + self.user + "," + self.base_dn
        bind_pw = self.pwd
        try:
            self.ldap_server.protocol_version = ldap.VERSION3   # pylint: disable=no-member
            self.ldap_server.simple_bind_s(bind_dn, bind_pw)
        except ldap.LDAPError as error:   # pylint: disable=no-member
            print(error)
            sys.exit("LDAP Connection failed; exiting")
        return True

    def get_all_users(self):
        search_filter = "(&(objectClass=" + LDAPUser.OBJECT_CLASS + ")"
        if LDAPUser.NON_USER_GROUPS:
            search_filter += "(!"
            for group in LDAPUser.NON_USER_GROUPS:
                search_filter += "(memberOf=cn=" + group + "," + self.base_dn + ")"
            search_filter += ")"
        search_filter += ")"

        return self.do_search(search_filter, LDAPUser.OBJECT_CLASS)

    def get_users_by_uid(self, uids):
        search_filter = ""
        if not isinstance(uids, list):
            search_filter = "(uid=" + uids + ")"
        else:
            search_filter += "(|"
            for uid in uids:
                search_filter += "(uid=" + uid + ")"
            search_filter += ")"

        return self.do_search(search_filter, LDAPUser.OBJECT_CLASS)

    def get_users_by_group(self, gcns):
        search_filter = "(&(objectClass=" + LDAPUser.OBJECT_CLASS + ")"
        if not isinstance(gcns, list):
            search_filter += "(memberOf=cn=" + gcns + "," + self.base_dn + ")"
        else:
            search_filter += "(|"
            for gcn in gcns:
                search_filter += "(memberOf=cn=" + gcn + "," + self.base_dn + ")"
            search_filter += ")"
        search_filter += ")"

        return self.do_search(search_filter, LDAPUser.OBJECT_CLASS)

    def get_groups(self, groups=None):
        search_filter = "(&(objectClass=" + LDAPGroup.OBJECT_CLASS + ")"
        if groups:
            for group in groups:
                search_filter += "(cn=" + group + ")"
        search_filter += ")"

        return self.do_search(search_filter, LDAPGroup.OBJECT_CLASS)

    def do_search(self, search_filter, ldap_obj_class):
        search_scope = ldap.SCOPE_SUBTREE   # pylint: disable=no-member
        result_set = []

        if self.ldap_server is None:
            print("No server present, binding to default server")
            self.bind_server()

        if ldap_obj_class not in [LDAPUser.OBJECT_CLASS, LDAPGroup.OBJECT_CLASS]:
            raise LDAPObjectException((
                'LDAP Object Class must be %s or %s',
                LDAPUser.OBJECT_CLASS,
                LDAPGroup.OBJECT_CLASS
            ))

        try:
            result_id = self.ldap_server.search(
                self.base_dn,
                search_scope,
                search_filter
            )
            while 1:
                result_type, result_data = self.ldap_server.result(result_id, 0)
                if not result_data:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:   # pylint: disable=no-member
                        if ldap_obj_class == LDAPUser.OBJECT_CLASS:
                            result_set.append(LDAPUser(**result_data[0][1]))
                        elif ldap_obj_class == LDAPGroup.OBJECT_CLASS:
                            result_set.append(LDAPGroup(**result_data[0][1]))
        except ldap.LDAPError as error:   # pylint: disable=no-member
            print(error)
            sys.exit("LDAP Connection failed; exiting")
        return result_set

    def unbind_server(self):
        self.ldap_server.unbind_s()
        self.ldap_server = None
