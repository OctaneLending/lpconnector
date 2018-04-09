from __future__ import print_function
from .basecommand import BaseCommand


class Provision(BaseCommand):   # pylint: disable=too-few-public-methods

    """
    Usage:
        provision [--users=UIDs | --groups=GCNs] [--url=URL] [--password=PWD]
            [--no-reset-password] [--dry-run]


        -n --dry-run            Display API requests instead of sending them
        -u UIDS --users=UIDs    Comma separated list of user uids to provision/sync
        -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces
        --url=URL               Specify API endpoint URL
        --password=PWD   Default password for provisioned users
        --no-reset-password     Do not reset the default password

    """

    def execute(self):
        self.bind_ldap()

        new_users = []
        if self.args.get('--users') is None and self.args.get('--groups') is None:
            print("Provisioning ALL users...")
            new_users = self.ldap_server.get_all_users()
        if self.args.get('--users') is not None:
            users = self.args.get('--users').split(',')
            print("Provisioning " + str(len(users)) + " user(s)...")
            new_users = self.ldap_server.get_users_by_uid(users)

        if self.args.get('--groups') is not None:
            groups = self.args.get('--groups').split(',')
            print("Provisioning " + str(len(groups)) + " group(s)...")
            new_users = self.ldap_server.get_users_by_group(groups)

        print("Retrieved " + str(len(new_users)) + " to user(s) provision...")
        self.unbind_ldap()

        password = self.args.get('--password')
        no_reset = self.args.get('--no-reset-password')
        if self.lp_client.batch_add(new_users, password, no_reset):
            print(str(len(new_users)) + " user(s) successfully provisioned.")
        else:
            exit("Provisioning failed; exiting")
        return True
