from __future__ import print_function
from distutils.util import strtobool
from .basecommand import BaseCommand


class LastPassUsers(BaseCommand):   # pylint: disable=too-few-public-methods
    """
    Get users in LastPass

    Usage:
        lastpassusers [options]

        -n --dry-run            Display API requests instead of sending them
        --url=URL               Specify API endpoint URL
        --email=EMAIL           Get a single user by their email address
        --disabled=BOOL         Get only disabled users
        --admin=BOOL            Get only admin users

    """

    def execute(self):
        disabled = strtobool(self.args.get('--disabled')) if self.args.get('--disabled') else None
        admin = strtobool(self.args.get('--admin')) if self.args.get('--admin') else None
        users = self.lp_client.get_user_data(
            user=self.args.get('--email'),
            disabled=disabled,
            admin=admin
        )
        for user in users:
            print(user.as_dict())
        return True
