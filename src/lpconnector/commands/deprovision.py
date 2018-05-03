from __future__ import print_function
from .basecommand import BaseCommand
from ..lastpass.objects import LastPassUser

class Deprovision(BaseCommand):
    """
    Remove a user from LastPass

    Usage:
        deprovision --email=EMAIL [--action=INT | --deactivate | --remove | --delete] [--dry-run]

        -n --dry-run    Display API requests instead of sending them
        --email=EMAIL   Delete the specified user
        --action=INT    Specify the delete action (0, 1, or 2) [default: 0]
        --deactivate    Blocks login but retains data and membership (same as --action=0)
        --remove        Removes the user from enterprise but keeps account active (same as --action=1)
        --delete        Completely delete the account (same as --action=2)

    """

    # Delete action codes
    DEACTV_ACT = 0
    REMOVE_ACT = 1
    DELETE_ACT = 2

    ACTION_CODES = {0: 'DEACTIVATE', 1: 'REMOVE', 2: 'DELETE'}

    def execute(self):
        email = self.args.get('--email')
        print("Deprovisioning user " + email + "...")
        lp_user = self.lp_client.get_user_data(email)[0]
        if not isinstance(lp_user, LastPassUser):
            print("User not present.")
            return False
        if lp_user.disabled:
            if not self.confirmation_prompt('User is already disabled.'):
                print('Exiting deprovisioning.')
                return False

        action_code = int(self.args.get('--action')) if self.args.get('--action') else None
        if self.args.get('--deactivate'):
            action_code = self.DEACTV_ACT
        if self.args.get('--remove'):
            action_code = self.REMOVE_ACT
        if self.args.get('--delete'):
            action_code = self.DELETE_ACT

        if action_code and action_code not in [self.DEACTV_ACT, self.REMOVE_ACT, self.DELETE_ACT]:
            action_code = 0

        print('Deprovision action set to ' + self.ACTION_CODES.get(action_code) + ' (' + str(action_code) + ')')

        if self.confirmation_prompt('Set to ' + self.ACTION_CODES.get(action_code) + ' user ' + email + '.'):
            if self.lp_client.delete_user(email, action_code):
                print(email + ' successfully deprovisioned.')
                return True
            print('Failed to delete user.')
            return False
        print('Exiting deprovisioning.')
        return False
