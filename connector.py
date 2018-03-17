"""LastPass Connector

Usage:
    connector.py sync
    connector.py provision [--users=UIDS] [--password=PWD] [--reset-password=BOOL]
    connector.py getldapusers [--users=UIDS]
    connector.py getlastpassusers [--email=EMAIL] [--disabled=BOOL] [--admin=BOOL]
    connector.py (-h | --help)

Options:
    -h --help               Show help
    --users=UIDS            Comma separated list of uids to provision
    --password=PWD          Default password for provisioned users
    --reset-password=BOOL   Reset the default password [default: True]
    --email=EMAIL           Get a single user by their full email address
    --disabled=BOOL         Get only disabled users
    --admin=BOOL            Get only admin users
"""

from docopt import docopt
from dotenv import load_dotenv
from distutils.util import strtobool
from ldap_server import LDAPServer
from lastpass_client import LastPassClient
from lastpass_sync import LastPassSyncer
from lastpass_provision import LastPassProvisioner

if __name__ == "__main__":
    load_dotenv()
    args = docopt(__doc__)

    if args.get('sync'):
        print "Syncing LastPass to LDAP..."
        syncer = LastPassSyncer()
        syncer.run()

    if args.get('provision'):
        users = None
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        password = args.get('--password')
        resetPwd = strtobool(args.get('--reset-password'))
        provisioner = LastPassProvisioner(users, password, resetPwd)
        provisioner.run()

    if args.get('getldapusers'):
        users = None
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        if users:
            print "Retrieving " + str(len(users)) + " users from the directory..."
        else:
            print "Retrieving all users from the directory..."

        ldapServer = LDAPServer()
        ldapServer.bindToServer()
        result = []
        if users is None:
            result = ldapServer.getAllUsers()
        else:
            result = ldapServer.getUsersByUID(users)
        ldapServer.unbindServer()
        for ldapUser in result:
            print ldapUser

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

        lpClient = LastPassClient()
        lpClient.getUserData(user, disabled, admin)
