from .basecommand import BaseCommand
from ..lastpass.client import LastPassClient


class LastPassGroups(BaseCommand):
    """
    Display groups in LastPass

    Usage:
        lastpassgroups [options]

        -n --dry-run            Display API requests instead of sending them
        -v --verbose            Print verbose output  # default True if dry-run enabled
        -u URL --url=URL        Specify API endpoint URL

    """

    def execute(self):
        lp_client = LastPassClient(
            cid=self.config.get('LASTPASS', 'API_CID'),
            user=self.config.get('LASTPASS', 'API_USER'),
            key=self.config.get('LASTPASS', 'API_SECRET'),
            dry_run=self.args.get('--dry-run')
        )
        groups = lp_client.get_group_data()
        for group in groups:
            print group.__dict__
        return True
