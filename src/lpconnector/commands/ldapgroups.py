from .basecommand import BaseCommand


class LDAPGroups(BaseCommand):  # pylint: disable=too-few-public-methods
    """
    Display groups in LDAP

    Usage:
        ldapgroups [options]

        -v --verbose            Print verbose output

    """

    def execute(self):
        self.bind_ldap()
        groups = self.ldap_server.get_all_groups()
        self.unbind_ldap()
        for group in groups:
            print group.as_dict()
        return True
