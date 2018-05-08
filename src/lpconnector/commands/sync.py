from __future__ import print_function
from time import sleep
from .basecommand import BaseCommand


class Sync(BaseCommand):    # pylint: disable=too-few-public-methods

    """
    Usage:
        sync [--users=UIDs | --groups=GCNs] [--url=URL] [--throttle=NUM] [--no-add] [--no-delete] [--no-update]
            [--dry-run]


        -n --dry-run            Display API requests instead of sending them
        -u UIDS --users=UIDs    Comma separated list of user uids to provision/sync
        -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces
        --url=URL               Specify API endpoint URL
        -t NUM --throttle=NUM   Throttle loading by specified value [default: 0]
        --no-add                Don't add new users on sync
        --no-delete             Don't delete missing users on sync
        --no-update             Don't update a user's groups on sync

    """

    def __init__(self, command, command_args):
        super(Sync, self).__init__(command, command_args)
        self.bind_ldap()
        self.ldap_users = []
        self.lastpass_users = []

    def execute(self):
        if self.args.get('--users') is None and self.args.get('--groups') is None:
            print("Syncing ALL users to LastPass...")
            self.ldap_users = self.ldap_server.get_all_users()
            print("Retrieving " + str(len(self.ldap_users)) + " LDAP Users...")
            self.lastpass_users = self.lp_client.get_user_data()
        else:
            if self.args.get('--users') is not None:
                users = self.args.get('--users').split(',')
                print("Syncing " + str(len(users)) + " user(s)...")
                self.ldap_users = self.ldap_server.get_users_by_uid(users)
            if self.args.get('--groups') is not None:
                groups = self.args.get('--groups').split(',')
                print("Syncing " + str(len(groups)) + " group(s)...")
                self.ldap_users = self.ldap_server.get_users_by_group(groups)
            print("Retrieving " + str(len(self.ldap_users)) + " LDAP Users...")

            ldap_user_emails = [user.get_email() for user in self.ldap_users]
            for email in ldap_user_emails:
                lp_user = self.lp_client.get_user_data(email)
                if lp_user:
                    self.lastpass_users.append(lp_user[0])
        self.unbind_ldap()
        print("Retrieved " + str(len(self.lastpass_users)) + " LastPass Users...")

        return self.sync()

    def sync(self):
        if not self.args.get('--no-add'):
            self.add_new_users()

        if not self.args.get('--no-delete'):
            self.del_old_users()

        if not self.args.get('--no-update'):
            self.sync_user_groups()

        return True

    def add_new_users(self):
        new_users = self.get_new_users()
        if new_users:
            print(str(len(new_users)) + " user(s) to add...")
            throttle = int(self.args.get('--throttle'))
            if self.lp_client.batch_add(new_users, throttle):
                print(str(len(new_users)) + " user(s) successfully added...")
            else:
                print("Failed to add users")
                return False
        else:
            print("No users to add")
        return True

    def del_old_users(self):
        del_users = self.get_del_users()
        if del_users:
            print(str(len(del_users)) + " user(s) to delete...")
            throttle = int(self.args.get('--throttle'))
            count = 0
            for user in del_users:
                if throttle and count == throttle:
                    sleep(1)
                    count = 0
                if self.lp_client.delete_user(user.get_email()):
                    print(user.get_email() + " successfully deactivated...")
                    count += 1
                else:
                    print("Failed to delete " + user.get_email())
                    return False
        else:
            print("No users to delete")
        return True

    def sync_user_groups(self):
        synced_users = self.get_synced_users()
        print(str(len(synced_users)) + " user(s) to sync...")
        lp_user_dict = {}
        for lp_user in self.lastpass_users:
            lp_user_dict[lp_user.get_email()] = lp_user

        user_payload = []
        for user in synced_users:
            update = False
            payload_dict = {'username': user.get_email()}
            ldap_groups = user.groups
            lp_groups = lp_user_dict.get(user.get_email()).groups
            new_groups = ldap_groups
            del_groups = []

            if lp_groups:
                new_groups = [x for x in ldap_groups if x not in lp_groups]
                del_groups = [y for y in lp_groups if y not in ldap_groups]

            if new_groups:
                payload_dict['add'] = new_groups
                update = True
            if del_groups:
                payload_dict['del'] = del_groups
                update = True
            if update:
                user_payload.append(payload_dict)

        if user_payload:
            if self.lp_client.sync_groups(user_payload):
                print(str(len(user_payload)) + " user(s) successfully synced...")
                return True
            else:
                exit("Syncing failed; exiting")
        else:
            print("All users up to date...")

        return True

    def get_new_users(self):
        lastpass_emails = set(x.get_email() for x in self.lastpass_users)
        new_users = [y for y in self.ldap_users if y.get_email() not in lastpass_emails]
        return new_users

    def get_del_users(self):
        ldap_emails = set(x.get_email() for x in self.ldap_users)
        del_users = [y for y in self.lastpass_users if y.get_email() not in ldap_emails]
        return del_users

    def get_synced_users(self):
        lastpass_emails = set(x.get_email() for x in self.lastpass_users)
        synced_users = [y for y in self.ldap_users if y.get_email() in lastpass_emails]
        return synced_users
