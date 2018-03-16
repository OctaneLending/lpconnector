"""LastPass Connector

Usage:
    connector.py sync
    connector.py provision [--users=UIDS] [--password=PWD] [--reset-password=BOOL]
    connector.py (-h | --help)

Options:
    -h --help               Show help
    --users=UIDS            Comma separated list of uids to provision
    --password=PWD          Default password for provisioned users
    --reset-password=BOOL   Reset the default password [default: True]
"""

from docopt import docopt
from dotenv import load_dotenv
from distutils.util import strtobool
from lastpass_sync import LastPassSyncer
from lastpass_provision import LastPassProvisioner

if __name__ == "__main__":
    load_dotenv()
    args = docopt(__doc__)
    print(args)
    if args.get('sync'):
        syncer = LastPassSyncer()
        syncer.run()

    if args.get('provision'):
        users = None
        if args.get('--users') is not None:
            users = args.get('--users').split(',')
        password = args.get('--password')
        resetPwd = strtobool(args.get('--reset-password'))
        print users
        print password
        print resetPwd
        provisioner = LastPassProvisioner(users, password, resetPwd)
        provisioner.run()
