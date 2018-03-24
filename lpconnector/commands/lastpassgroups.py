from .basecommand import BaseCommand


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
        groups = self.lp_client.get_group_data()
        for group in groups:
            print group.__dict__
        return True
