from .basecommand import BaseCommand


class LastPassUsers(BaseCommand):
    """
    Get users in LastPass

    Usage:
        lastpassusers [options]

        -n --dry-run            Display API requests instead of sending them
        -v --verbose            Print verbose output  # default True if dry-run enabled
        --url=URL               Specify API endpoint URL
        --email=EMAIL           Get a single user by their email address
        --disabled              Get only disabled users
        --admin                 Get only admin users

    """

    def execute(self):
        users = self.lp_client.get_user_data(
            user=self.args.get('--email'),
            disabled=self.args.get('--disabled'),
            admin=self.args.get('--admin')
        )
        for user in users:
            print user.__dict__
        return True
