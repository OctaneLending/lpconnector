import re
from docopt import docopt
from ..base.config import BaseConfig
from ..ldap.server import LDAPServer
from ..lastpass.client import LastPassClient


class BaseCommand(object):
    """
    Base class for commands

    Usage:
    """

    # map command names to classes in the commands modules
    COMMAND_MAP = {
        'sync': {
            'class': 'Sync',
            'argv': True,
        },
        'config': {
            'class': 'Config',
            'argv': False,
        },
        'provision': {
            'class': 'Provision',
            'argv': True,
        },
        'deprovision': {
            'class': 'Deprovision',
            'argv': True,
        },
        'ldapusers': {
            'class': 'LDAPUsers',
            'argv': True,
        },
        'ldapgroups': {
            'class': 'LDAPGroups',
            'argv': True,
        },
        'lastpassusers': {
            'class': 'LastPassUsers',
            'argv': True,
        },
        'lastpassgroups': {
            'class': 'LastPassGroups',
            'argv': True,
        },
    }

    def __init__(self, command, command_args):
        self.config = BaseConfig()
        if BaseCommand.COMMAND_MAP.get(command).get('argv'):
            self.args = docopt(self.__doc__, argv=command_args)
        else:
            self.args = docopt(self.__doc__)

        self.ldap_server = LDAPServer(
            config=self.config.ldap()
        )

        url = self.args.get('--url')
        self.lp_client = LastPassClient(
            dry_run=self.args.get('--dry-run'),
            url=url if url is not None else LastPassClient.DEFAULT_ENDPOINT,
            config=self.config.lastpass()
        )

    def bind_ldap(self):
        self.ldap_server.bind_server()

    def unbind_ldap(self):
        self.ldap_server.unbind_server()

    def execute(self):
        raise NotImplementedError

    @staticmethod
    def confirmation_prompt(message):
        response = raw_input(message + ' Continue? [y/n]: ')
        return True if re.match(r"^y(?=e?$|e(?![^s]))", response, re.IGNORECASE) else False
