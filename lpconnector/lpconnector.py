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

See `lpconnector help <comnmand>` for more information on a specific command

"""

import os,sys,ConfigParser
from docopt import docopt
from subprocess import call
from distutils.util import strtobool
from importlib import import_module
from .ldap.server import LDAPServer
from .lastpass.client import LastPassClient
from .lastpass.sync import LastPassSyncer
from .lastpass.provision import LastPassProvisioner
from .commands.basecommand import BaseCommand


def main():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.abspath('lpconnector'), 'config/config.ini'))
    args = docopt(__doc__, version='lpconnector v0.1.0', options_first=True)
    command_name = args.pop('<command>')
    argv = args.pop('<args>')

    if command_name in BaseCommand.COMMAND_MAP.keys():
        module_name = '.commands.%s' % command_name
        module = import_module(module_name, 'lpconnector')
        try:
            command_class = getattr(module, BaseCommand.COMMAND_MAP.get(command_name).get('class'))
        except AttributeError:
            sys.exit('Command module not found; exiting.')
        command = command_class(config, command_name, argv)
        command.execute()
    elif args['<command>'] in ['help', None]:
        exit(call(['lpconnector', '--help']))
    else:
        sys.exit("%r is not a valid command. See `lpconnector help`." % args['<command>'])

    return

    if args.get('sync'):
        users = None
        groups = None
        byGroup = False
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        if args.get('--groups') is not None:
            groups = args.get('--groups').split(',')
            byGroup = True
        if byGroup:
            syncer = LastPassSyncer(config, groups, byGroup)
        else:
            syncer = LastPassSyncer(config, users)
        if syncer.run():
            print "Completed!"
        return

    if args.get('provision'):
        users = None
        groups = None
        byGroup = False
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        if args.get('--groups') is not None:
            groups = args.get('--groups').split(',')
            byGroup = True
        if byGroup:
            provisioner = LastPassProvisioner(config, groups, byGroup)
        else:
            provisioner = LastPassProvisioner(config, users)
        if provisioner.run():
            print "Completed!"
        return
