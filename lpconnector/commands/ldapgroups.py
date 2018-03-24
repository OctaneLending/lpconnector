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
        ldap_server = LDAPServer(
            host=self.config.get('LDAP', 'SERVER'),
            base_dn=self.config.get('LDAP', 'BASE_DN'),
            user=self.config.get('LDAP', 'BINDING_USER_UID'),
            pwd=self.config.get('LDAP', 'BINDING_USER_PWD')
        )
        ldap_server.bind_server()
        groups = ldap_server.get_all_groups()
        for group in groups:
            print group.__dict__
        return True
