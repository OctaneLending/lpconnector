"""
Usage:
    lpconnector provision [--users=UIDs | --groups=GCNs] [--password=PWD] [--no-reset-password]

Options:
    -u UIDS --users=UIDs    Comma separated list of user uids to provision/sync
    -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces
    -p PWD --password=PWD   Default password for provisioned users
    --no-reset-password     Do not reset the default password

"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))