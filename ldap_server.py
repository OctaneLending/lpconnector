import ldap
from ldap_user import LDAPUser
from ldap_group import LDAPGroup

class LDAPServer(object):

    def __init__(self, server, baseDN, user, pwd):
        self.server = server
        self.baseDN = baseDN
        self.user = user
        self.pwd = pwd
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
        searchFilter = "(&(objectClass=" + LDAPUser.objectClass + "))"
        searchAttributes = LDAPUser.attributes

        return self.doSearch(searchFilter, searchAttributes, 'user')

    def getAllGroups(self):
        searchFilter = "(&(objectClass=" + LDAPGroup.objectClass + "))"
        searchAttributes = LDAPGroup.attributes

        return self.doSearch(searchFilter, searchAttributes, 'group')

    def doSearch(self, sFilter, sAttributes, returnType):
        print sFilter + ' : ' + ', '.join(sAttributes)
        sScope = ldap.SCOPE_SUBTREE
        result_set = []

        if self.ldapServer is not None:
            try:
                result_id = self.ldapServer.search(self.baseDN, sScope, sFilter, sAttributes)
                while 1:
                    result_type, result_data = self.ldapServer.result(result_id, 0)
                    if (result_data == []):
                        break
                    else:
                        if result_type == ldap.RES_SEARCH_ENTRY:
                            print result_data[0][1]
                            if returnType == 'user':
                                result_set.append(LDAPUser(**result_data[0][1]))
                            elif returnType == 'group':
                                result_set.append(LDAPGroup(**result_data[0][1]))
            except ldap.LDAPError, error:
                print error

        return result_set

    def unbindServer(self):
        self.ldapServer.unbind_s()
        self.ldapServer = None
