from distutils.util import strtobool
from ..ldap.server import LDAPServer
from .client import LastPassClient

class LastPassSyncer(object):

    def __init__(self, config, usersOrGroups, byGroup = False):
        self.usersOrGroups = usersOrGroups
        self.byGroup = byGroup
        self.noAdd = strtobool(config.get('ARGS', 'no-add'))
        self.noDel = strtobool(config.get('ARGS', 'no-delete'))
        self.noUp = strtobool(config.get('ARGS', 'no-update'))
        self.client = LastPassClient(config)
        self.server = LDAPServer(config)
        return

    def run(self):
        self.server.bindToServer()
        ldapUsers = []
        lastPassUsers = []
        userCount = 0
        if self.usersOrGroups is None:
            print "Syncing ALL users to LastPass..."
            ldapUsers = self.server.getAllUsers()
            print "Retrieving " + str(len(ldapUsers)) + " LDAP Users..."
            lastPassUsers = self.client.getUserData()
            print "Retrieving " + str(len(lastPassUsers)) + " LastPass Users..."
        else:
            count = len(self.usersOrGroups)
            if self.byGroup:
                print "Syncing " + str(count) + " group[s]..."
                ldapUsers = self.server.getUsersByGroup(self.usersOrGroups)
                print "Retrieving " + str(len(ldapUsers)) + " LDAP Users..."
            else:
                print "Syncing " + str(count) + " user[s]..."
                ldapUsers = self.server.getUsersByUID(self.usersOrGroups)
                print "Retrieving " + str(len(ldapUsers)) + " LDAP Users..."
            ldapUserEmails = map(lambda x: x.email, ldapUsers)
            for email in ldapUserEmails:
                lpUser = self.client.getUserData(email)
                if len(lpUser) > 0:
                    lastPassUsers.append(self.client.getUserData(email)[0])
            print "Retrieving " + str(len(lastPassUsers)) + " LastPass Users..."

        self.server.unbindServer()

        newUsers = []
        delUsers = []
        if not self.noAdd:
            newUsers = self.getNewUsers(ldapUsers, lastPassUsers)
        if not self.noDel:
            delUsers = self.getDelUsers(ldapUsers, lastPassUsers)
        print str(len(newUsers)) + " user[s] to add..."
        print str(len(delUsers)) + " user[s] to delete..."

        self.sync(newUsers, delUsers)
        return

    def sync(self, newUsers, delUsers):
        return

    def getNewUsers(self, ldapUsers, lastPassUsers):
        lastPassEmails = set(x.username for x in lastPassUsers)
        newUsers = [y for y in ldapUsers if y.email not in lastPassEmails]
        return newUsers

    def getDelUsers(self, ldapUsers, lastPassUsers):
        ldapEmails = set(x.email for x in ldapUsers)
        delUsers = [y for y in lastPassUsers if y.username not in ldapEmails]
        return delUsers

