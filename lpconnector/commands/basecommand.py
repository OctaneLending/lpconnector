from docopt import docopt
from ..ldap.server import LDAPServer
from ..lastpass.client import LastPassClient


class BaseCommand(object):
    """Base class for commands"""

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

    def __init__(self, config, command, command_args):
        self.config = config
        if BaseCommand.COMMAND_MAP.get(command).get('argv'):
            self.args = docopt(self.__doc__, argv=command_args)
        else:
            self.args = docopt(self.__doc__)
        self.verbose = self.args.get('--verbose')

        self.ldap_server = LDAPServer(
            config=self.config.items('LDAP')
        )

        url = self.args.get('--url')
        self.lp_client = LastPassClient(
            dry_run=self.args.get('--dry-run'),
            url=url if url is not None else LastPassClient.DEFAULT_ENDPOINT,
            config=self.config.items('LASTPASS')
        )

    def execute(self):
        raise NotImplementedError
