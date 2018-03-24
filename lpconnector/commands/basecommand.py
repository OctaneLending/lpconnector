from docopt import docopt


class BaseCommand:
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

    def execute(self):
        raise NotImplementedError

