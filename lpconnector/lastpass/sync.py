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
            print "Retrieved " + str(len(lastPassUsers)) + " LastPass Users..."
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
            print "Retrieved " + str(len(lastPassUsers)) + " LastPass Users..."

        self.server.unbindServer()
        print ldapUsers
        print lastPassUsers
        self.sync(ldapUsers, lastPassUsers)
        return

    def sync(self, ldapUsers, lastPassUsers):
        if not self.noAdd:
            newUsers = self.getNewUsers(ldapUsers, lastPassUsers)
            print str(len(newUsers)) + " user[s] to add..."
            response = self.client.batchAdd(newUsers)
            if response.status_code == 200:
                print str(len(newUsers)) + " user[s] successfully added..."
            else:
                response.raise_for_status()
        if not self.noDel:
            delUsers = self.getDelUsers(ldapUsers, lastPassUsers)
            print str(len(delUsers)) + " user[s] to delete..."
            for user in delUsers:
                response = self.client.deleteUser(user.username)
                if response.status_code == 200:
                    print user.username + " successfully deactivated..."
                else:
                    response.raise_for_status()
        if not self.noUp:
            syncedUsers = self.getSyncedUsers(ldapUsers, lastPassUsers)
            print str(len(syncedUsers)) + " user[s] to sync..."
            ldapUserDict = {}
            for user in ldapUsers:
                ldapUserDict['user.email'] = user


        return

    def getNewUsers(self, ldapUsers, lastPassUsers):
        lastPassEmails = set(x.username for x in lastPassUsers)
        newUsers = [y for y in ldapUsers if y.email not in lastPassEmails]
        return newUsers

    def getDelUsers(self, ldapUsers, lastPassUsers):
        ldapEmails = set(x.email for x in ldapUsers)
        delUsers = [y for y in lastPassUsers if y.username not in ldapEmails]
        return delUsers

    def getSyncedUsers(self, ldapUsers, lastPassUsers):
        lastPassEmails = set(x.username for x in lastPassUsers)
        syncedUsers = [y for y in ldapUsers if y.email in lastPassEmails]
        return syncedUsers

