from .basecommand import BaseCommand
from ..lastpass.client import LastPassClient


class LastPassUsers(BaseCommand):
    """
    Get users in LastPass

    Usage:
        lastpassusers [options]

        -n --dry-run            Display API requests instead of sending them
        -v --verbose            Print verbose output  # default True if dry-run enabled
        -u URL --url=URL        Specify API endpoint URL
        -e EMAIL --email=EMAIL   Get a single user by their email address
        --disabled              Get only disabled users
        --admin                 Get only admin users

    """

    def execute(self):
        lp_client = LastPassClient(
            cid=self.config.get('LASTPASS', 'API_CID'),
            user=self.config.get('LASTPASS', 'API_USER'),
            key=self.config.get('LASTPASS', 'API_SECRET'),
            dry_run=self.args.get('--dry-run')
        )
        users = lp_client.get_user_data(
            user=self.args.get('--email'),
            disabled=self.args.get('--disabled'),
            admin=self.args.get('--admin')
        )
        for user in users:
            print user.__dict__
        return True
