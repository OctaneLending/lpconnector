import os

from ldap_server import LDAPServer
from lastpass_client import LastPassClient

class LastPassProvisioner(object):

    def __init__(self, users, password, resetPwd):
        self.users = users
        self.password = password
        self.resetPwd = resetPwd
        self.client = LastPassClient()
        self.server = LDAPServer(
                os.getenv("LDAP_SERVER"),
                os.getenv("LDAP_BASE_DN"),
                os.getenv("LDAP_BINDING_USER_UID"),
                os.getenv("LDAP_BINDING_USER_PWD"))

    def run(self):
        self.server.bindToServer()
        newUsers = []
        if self.users is None:
            newUsers = ldapServer.getAllUsers()
        else:
            for uid in self.users:
                newUsers.append(self.server.getUserByUID(uid)[0])
        self.server.unbindServer()
        self.client.batchAdd(newUsers, self.password, self.resetPwd)

