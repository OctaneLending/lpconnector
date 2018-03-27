from importlib import import_module
from subprocess import call
import docopt
from . import __version__
from .config.config import Config
from .commands.basecommand import BaseCommand


class LPConnector(object):

    """
    LastPass Connector

    Usage: lpconnector [options] <command> [<args>...]

    Options:
        --version               Print package version and exit
        -h --help               Show command help and exit
        -c FILE --config=FILE   Specify configuration file path

    Commands:
        sync            Sync LDAP users and groups with LastPass Enterprise
        provision       Add LDAP users and groups to LastPass Enterprise
        ldapusers       Return LDAP users
        ldapgroups      Return LDAP groups
        lastpassusers   Return LastPass users
        lastpassgroups  Return LastPass groups
        config          Display configuration settings

    See `lpconnector help <command>` for more information on a specific command

    """

    def __init__(self, args=None):
        version = "lpconnector v" + __version__
        self.args = docopt.docopt(self.__doc__, argv=args, version=version, options_first=True)
        self.config = Config(self.args.get('--config'))

    def main(self):
        command_name = self.args.pop('<command>')
        argv = self.args.pop('<args>')

        if command_name in BaseCommand.COMMAND_MAP.keys():
            command_class = self.get_command_class(command_name)
            command = command_class(command_name, argv)
            command.execute()
        elif command_name == 'help':
            if len(argv) == 1:
                subcommand = argv[0]
                if subcommand in BaseCommand.COMMAND_MAP.keys():
                    subcommand_class = self.get_command_class(subcommand)
                    exit(subcommand_class.__doc__)
            exit(call(['lpconnector', '--help']))
        else:
            raise docopt.DocoptExit("%r is not a valid command. See `lpconnector help`." % command_name)

        exit("Command: " + command_name + "; Complete.")

    @staticmethod
    def get_command_class(command_name):
        module_name = '.commands.%s' % command_name
        module = import_module(module_name, 'lpconnector')
        try:
            command_class = getattr(module, BaseCommand.COMMAND_MAP.get(command_name).get('class'))
        except AttributeError:
            print 'Command module not found'
            return None
        return command_class
