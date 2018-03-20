"""LastPass Connector

Usage:
    lpconnector sync [--users=UIDs | --groups=GIDs] [--no-add] [--no-delete] [--no-update]
    lpconnector provision [--users=UIDs | --groups=GIDs] [--password=PWD] [--reset-password=BOOL]
    lpconnector getldapusers [--users=UIDs]
    lpconnector getlastpassusers [--email=EMAIL] [--disabled=BOOL] [--admin=BOOL]
    lpconnector getconfig
    lpconnector  (-h | --help)

Options:
    -h --help               Show help
    --users=UIDs            Comma separated list of uids to provision/sync
    --groups=GIDs           Comman seprated list of group names to provision/sync
    --no-add                Don't add new users on sync
    --no-delete             Don't delete missing users on sync
    --no-update             Don't update a user's groups on sync
    --password=PWD          Default password for provisioned users
    --reset-password=BOOL   Reset the default password [default: True]
    --email=EMAIL           Get a single user by their full email address
    --disabled=BOOL         Get only disabled users
    --admin=BOOL            Get only admin users
"""
import os,ConfigParser
from docopt import docopt
from distutils.util import strtobool
from .ldap.server import LDAPServer
from .lastpass.client import LastPassClient
from .lastpass.sync import LastPassSyncer
from .lastpass.provision import LastPassProvisioner

def getConfig(args):
    config = ConfigParser.ConfigParser()
    configPath = os.path.join(os.path.abspath(__path__), 'config/config.ini')
    print configPath
    configFile = open(configPath)
    print configFile.read()
    config.read(os.path.join(os.path.abspath(__path__), 'config/config.ini'))
    config.add_section('ARGS')
    for key, value in args.items():
        key = key[len('--'):] if key.startswith('--') else key
        config.set('ARGS', key, value)
    return config


def main():
    args = docopt(__doc__)
    config = getConfig(args)

    if args.get('getconfig'):
        print config.defaults()
        print config.sections()

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
        syncer.run()

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
        provisioner.run()

    if args.get('getldapusers'):
        users = None
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        if users:
            print "Retrieving " + str(len(users)) + " users from the directory..."
        else:
            print "Retrieving all users from the directory..."

        ldapServer = LDAPServer(config)
        ldapServer.bindToServer()
        result = []
        if users is None:
            result = ldapServer.getAllUsers()
        else:
            result = ldapServer.getUsersByUID(users)
        ldapServer.unbindServer()
        for ldapUser in result:
            print ldapUser.__dict__

    if args.get('getlastpassusers'):
        user = None
        if args.get('--email') is not None:
            user = args.get('--email')
        if user:
            print "Retrieving " + user + " from LastPass..."
        else:
            print "Retrieving all users from LastPass..."
        disabled = None
        if args.get('--disabled') is not None:
            disabled = 1 if strtobool(args.get('--disabled')) == True else 0
        admin = None
        if args.get('--admin') is not None:
            admin = 1 if strtobool(args.get('--admin')) == True else 0

        lpClient = LastPassClient(config)
        users = lpClient.getUserData(user, disabled, admin)
        print "Got " + str(len(users)) + " user[s]"

