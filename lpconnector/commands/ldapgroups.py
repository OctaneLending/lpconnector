from .basecommand import BaseCommand
from ..ldap.server import LDAPServer


class LDAPGroups(BaseCommand):
    """
    Display groups in LDAP
    
    Usage:
        ldapgroups [options]

        -v --verbose            Print verbose output
    
    """

    def execute(self):
        self.ldap_server.bind_server()
        groups = self.ldap_server.get_all_groups()
        self.ldap_server.unbind_server()
        for group in groups:
            print group.__dict__
        return True
