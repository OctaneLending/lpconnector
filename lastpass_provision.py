from ldap_server import LDAPServer
from lastpass_client import LastPassClient

class LastPassProvisioner(object):

    def __init__(self, users, password, resetPwd):
        self.users = users
        self.password = password
        self.resetPwd = resetPwd
        self.client = LastPassClient()
        self.server = LDAPServer()

    def run(self):
        self.server.bindToServer()
        newUsers = []
        if self.users is None:
            newUsers = self.server.getAllUsers()
        else:
            newUsers = self.server.getUsersByUID(self.users)
        self.server.unbindServer()
        self.client.batchAdd(newUsers, self.password, self.resetPwd)

