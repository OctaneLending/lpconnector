import ldap,os
from .user import LDAPUser
from .group import LDAPGroup

class LDAPServer(object):

    def __init__(self, server = None, baseDN = None, user = None, pwd = None):
        self.server = server if server else os.getenv("LDAP_SERVER")
        self.baseDN = baseDN if baseDN else os.getenv("LDAP_BASE_DN")
        self.user = user if user else os.getenv("LDAP_BINDING_USER_UID")
        self.pwd = pwd if pwd else os.getenv("LDAP_BINDING_USER_PWD")
        self.ldapServer = None

    def bindToServer(self):
        self.ldapServer = ldap.initialize(self.server)

        bindDN = "uid=" + self.user + "," + self.baseDN
        bindPW = self.pwd

        try:
            self.ldapServer.protocol_version = ldap.VERSION3
            self.ldapServer.simple_bind_s(bindDN, bindPW)
        except ldap.LDAPError, error:
            print error
        return self.ldapServer

    def getAllUsers(self):
        searchFilter = "(&(objectClass=" + LDAPUser.objectClass + ")(!(memberOf=cn=Service Accounts," + self.baseDN + ")))"

        return self.doSearch(searchFilter, LDAPUser.objectClass)

    def getAllGroups(self):
        searchFilter = "(&(objectClass=" + LDAPGroup.objectClass + "))"

        return self.doSearch(searchFilter, LDAPGroup.objectClass)

    def getUsersByUID(self, uids):
        searchFilter = ""
        if not isinstance(uids, list):
            searchFilter = "(uid=" + uids + ")"
        else:
            searchFilter += "(|"
            for uid in uids:
                searchFilter += "(uid=" + uid + ")"
            searchFilter += ")"
        searchAttributes = LDAPUser.attributes

        return self.doSearch(searchFilter, LDAPUser.objectClass)

    def getUsersByGroup(self, gids):
        searchFilter = "(&(objectClass=" + LDAPUser.objectClass + ")"
        if not isinstance(gids, list):
            searchFilter += "(memberOf=cn=" + gids + "," + self.baseDN + ")"
        else:
            searchFilter += "(|"
            for gid in gids:
                searchFilter += "(memberOf=cn=" + gid + "," + self.baseDN + ")"
            searchFilter += ")"
        searchFilter += ")"
        searchAttributes = LDAPUser.attributes

        return self.doSearch(searchFilter, LDAPUser.objectClass)

    def doSearch(self, sFilter, ldapObjClass):
        sScope = ldap.SCOPE_SUBTREE
        result_set = []

        if self.ldapServer is None:
            print "No server present, binding to default server"
            self.bindToServer()

        if ldapObjClass == LDAPUser.objectClass:
            sAttributes = LDAPUser.attributes
        elif ldapObjClass == LDAPGroup.objectClass:
            sAttributes = LDAPGroup.attributes
        else:
            print "Invalid search type, must be a user or a group"
            return result_set

        try:
            result_id = self.ldapServer.search(self.baseDN, sScope, sFilter, sAttributes)
            while 1:
                result_type, result_data = self.ldapServer.result(result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        if ldapObjClass == LDAPUser.objectClass:
                            result_set.append(LDAPUser(**result_data[0][1]))
                        elif ldapObjClass == LDAPGroup.objectClass:
                            result_set.append(LDAPGroup(**result_data[0][1]))
        except ldap.LDAPError, error:
            print error

        return result_set

    def unbindServer(self):
        self.ldapServer.unbind_s()
        self.ldapServer = None
