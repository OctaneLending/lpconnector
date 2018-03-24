from .basecommand import BaseCommand
from ..ldap.server import LDAPServer


class LDAPUsers(BaseCommand):
    """
    Display users in remote directory

    Usage:
        ldapusers [--verbose] [--users=UIDs | --groups=GCNs]

        -v --verbose            Print verbose output
        -u UIDS --users=UIDs    Comma separated list of user uids to provision/sync
        -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces

    """

    def execute(self):
        ldap_server = LDAPServer(
            host=self.config.get('LDAP', 'SERVER'),
            base_dn=self.config.get('LDAP', 'BASE_DN'),
            user=self.config.get('LDAP', 'BINDING_USER_UID'),
            pwd=self.config.get('LDAP', 'BINDING_USER_PWD')
        )
        ldap_server.bind_server()

        users = None
        groups = None
        by_group = False
        if self.args.get('--users') is not None:
            users = self.args.get('--users').split(',')
        if self.args.get('--groups') is not None:
            groups = self.args.get('--groups').split(',')
            by_group = True
        if users or groups:
            count = str(len(groups)) + " group[s]" if by_group else str(len(users)) + " user[s]"
            print "Retrieving " + count + " from the directory..."
        else:
            print "Retrieving all users from the directory..."

        result = []
        if by_group:
            result = ldap_server.get_users_by_group(groups)
        elif users is None:
            result = ldap_server.get_all_users()
        else:
            result = ldap_server.get_users_by_uid(users)
        ldap_server.unbind_server()
        for ldap_user in result:
            print ldap_user.__dict__
        return True
