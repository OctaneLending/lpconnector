import sys
import ldap
from .user import LDAPUser
from .group import LDAPGroup


class LDAPServer(object):

    def __init__(self, host, base_dn, user, pwd):
        self.host = host
        self.base_dn = base_dn
        self.user = user
        self.pwd = pwd
        self.ldap_server = None

    def bind_server(self):
        self.ldap_server = ldap.initialize(self.host)

        bind_dn = "uid=" + self.user + "," + self.base_dn
        bind_pw = self.pwd
        try:
            self.ldap_server.protocol_version = ldap.VERSION3
            self.ldap_server.simple_bind_s(bind_dn, bind_pw)
        except ldap.LDAPError, error:
            print error
            sys.exit("LDAP Connection failed; exiting")
        return True

    def get_all_users(self):
        search_filter = "(&(objectClass=" + LDAPUser.OBJECT_CLASS + ")"
        search_filter += "(!(memberOf=cn=Service Accounts," + self.base_dn + ")))"

        return self.do_search(search_filter, LDAPUser.OBJECT_CLASS)

    def get_all_groups(self):
        search_filter = "(&(objectClass=" + LDAPGroup.OBJECT_CLASS + "))"

        return self.do_search(search_filter, LDAPGroup.OBJECT_CLASS)

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

    def do_search(self, search_filter, ldap_obj_class):
        search_scope = ldap.SCOPE_SUBTREE
        result_set = []

        if self.ldap_server is None:
            print "No server present, binding to default server"
            self.bind_server()

        if ldap_obj_class == LDAPUser.OBJECT_CLASS:
            search_attributes = LDAPUser.ATTRIBUTES
        elif ldap_obj_class == LDAPGroup.OBJECT_CLASS:
            search_attributes = LDAPGroup.ATTRIBUTES
        else:
            print "Invalid search type, must be a user or a group"
            return result_set

        try:
            result_id = self.ldap_server.search(
                self.base_dn,
                search_scope,
                search_filter,
                search_attributes
            )
            while 1:
                result_type, result_data = self.ldap_server.result(result_id, 0)
                if result_data == []:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        if ldap_obj_class == LDAPUser.OBJECT_CLASS:
                            result_set.append(LDAPUser(**result_data[0][1]))
                        elif ldap_obj_class == LDAPGroup.OBJECT_CLASS:
                            result_set.append(LDAPGroup(**result_data[0][1]))
        except ldap.LDAPError, error:
            print error
            sys.exit("LDAP Connection failed; exiting")
        return result_set

    def unbind_server(self):
        self.ldap_server.unbind_s()
        self.ldap_server = None
