import sys
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
        if self.usersOrGroups is None:
            print "Syncing ALL users to LastPass..."
            ldapUsers = self.server.getAllUsers()
            print "Retrieving " + str(len(ldapUsers)) + " LDAP Users..."
            lastPassUsers = self.client.getUserData()
            print "Retrieved " + str(len(lastPassUsers)) + " LastPass Users..."
        else:
            count = len(self.usersOrGroups)
            if self.byGroup:
                print "Syncing " + str(count) + " group(s)..."
                ldapUsers = self.server.getUsersByGroup(self.usersOrGroups)
            else:
                print "Syncing " + str(count) + " user(s)..."
                ldapUsers = self.server.getUsersByUID(self.usersOrGroups)
            print "Retrieving " + str(len(ldapUsers)) + " LDAP Users..."
            ldapUserEmails = map(lambda x: x.email, ldapUsers)
            for email in ldapUserEmails:
                lpUser = self.client.getUserData(email)
                if len(lpUser) > 0:
                    lastPassUsers.append(self.client.getUserData(email)[0])
            print "Retrieved " + str(len(lastPassUsers)) + " LastPass Users..."

        self.server.unbindServer()
        if self.sync(ldapUsers, lastPassUsers):
            print "Syncing successful."
        else:
            print "Syncing failed."
        return True

    def sync(self, ldapUsers, lastPassUsers):
        if not self.noAdd:
            newUsers = self.getNewUsers(ldapUsers, lastPassUsers)
            if len(newUsers) > 0:
                print str(len(newUsers)) + " user(s) to add..."
                if self.client.batchAdd(newUsers):
                    print str(len(newUsers)) + " user(s) successfully added..."
                else:
                    print "Failed to add users"
                    return False
            else:
                print "No users to add"

        if not self.noDel:
            delUsers = self.getDelUsers(ldapUsers, lastPassUsers)
            if len(delUsers) > 0:
                print str(len(delUsers)) + " user(s) to delete..."
                for user in delUsers:
                    if self.client.deleteUser(user.username):
                        print user.username + " successfully deactivated..."
                    else:
                        print "Failed to delete " + user.username
                        return False
            else:
                print "No users to delete"

        if not self.noUp:
            syncedUsers = self.getSyncedUsers(ldapUsers, lastPassUsers)
            print str(len(syncedUsers)) + " user(s) to sync..."
            lpUserDict = {}
            for lp in lastPassUsers:
                lpUserDict[lp.username] = lp

            userPayload = []
            for user in syncedUsers:
                update = False
                payloadDict = {'username': user.email}
                ldapGroups = user.groups
                lpGroups = lpUserDict.get(user.email).groups
                newGroups = []
                delGroups = []

                if lpGroups:
                    newGroups = [x for x in ldapGroups if x not in lpGroups]
                    delGroups = [y for y in lpGroups if y not in ldapGroups]
                else:
                    newGroups = ldapGroups

                if len(newGroups) > 0:
                    payloadDict['add'] = newGroups
                    update = True
                if len(delGroups) > 0:
                    payloadDict['del'] = delGroups
                    update = True
                if update:
                    userPayload.append(payloadDict)

            if len(userPayload) > 0:
                if self.client.syncGroups(userPayload):
                    print str(len(userPayload)) + " user(s) successfully synced..."
                    return True
                else:
                    sys.exit("Syncing failed; exiting")
            else:
                print "No users to sync..."

        return True

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

