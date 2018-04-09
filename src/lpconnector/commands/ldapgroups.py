from __future__ import print_function
from .basecommand import BaseCommand


class LDAPGroups(BaseCommand):  # pylint: disable=too-few-public-methods
    """
    Display groups in LDAP

    Usage:
        ldapgroups [--groups=GCNs]

        -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces

    """

    def execute(self):
        self.bind_ldap()

        groups = None
        if self.args.get('--groups') is not None:
            groups = self.args.get('--groups').split(',')

        ldap_groups = self.ldap_server.get_groups(groups)

        self.unbind_ldap()

        for group in ldap_groups:
            print(group.as_dict())
        return True
