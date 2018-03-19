from ..ldap.server import LDAPServer
from .client import LastPassClient

class LastPassProvisioner(object):

    def __init__(self, usersOrGroups, password, resetPwd, byGroup = False):
        self.usersOrGroups = usersOrGroups
        self.byGroup = byGroup
        self.password = password
        self.resetPwd = resetPwd
        self.client = LastPassClient()
        self.server = LDAPServer()

    def run(self):
        self.server.bindToServer()
        newUsers = []
        userCount = 0
        if self.usersOrGroups is None:
            print "Provisioning ALL users..."
            newUsers = self.server.getAllUsers()
        else:
            if self.byGroup:
                groupCount = len(self.usersOrGroups)
                print "Provisioning " + str(groupCount) + " group[s]..."
                newUsers = self.server.getUsersByGroup(self.usersOrGroups)
            else:
                userCount = len(self.usersOrGroups)
                print "Provisioning " + str(userCount) + " user[s]..."
                newUsers = self.server.getUsersByUID(self.usersOrGroups)
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

