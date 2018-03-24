"""
Usage:
    lpconnector sync [--users=UIDs | --groups=GCNs] [--no-add] [--no-delete] [--no-update]

Options:
    -u UIDS --users=UIDs    Comma separated list of user uids to provision/sync
    -g GCNs --groups=GCNs   Comma separated list of group common names to provision/sync  # quote names with spaces
    --no-add                Don't add new users on sync
    --no-delete             Don't delete missing users on sync
    --no-update             Don't update a user's groups on sync

"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))