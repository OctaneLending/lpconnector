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
        userCount = 0
        if self.users is None:
            print "Provisioning ALL users..."
            newUsers = self.server.getAllUsers()
        else:
            userCount = len(self.users)
            print "Provisioning " + str(userCount) + " users..."
            newUsers = self.server.getUsersByUID(self.users)
        self.server.unbindServer()
        response = self.client.batchAdd(newUsers, self.password, self.resetPwd)
        if response.status_code == 200:
            if userCount == 0:
                print "ALL users successfully provisioned."
            elif userCount == 1:
                print "1 user successfully provisioned."
            else:
                print str(userCount) + " users successfully provisioned."
        else:
            response.raise_for_status()

