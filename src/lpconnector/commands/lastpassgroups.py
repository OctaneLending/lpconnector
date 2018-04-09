from .basecommand import BaseCommand


class LastPassGroups(BaseCommand):  # pylint: disable=too-few-public-methods
    """
    Display groups in LastPass

    Usage:
        lastpassgroups [options]

        -n --dry-run            Display API requests instead of sending them
        --url=URL               Specify API endpoint URL

    """

    def execute(self):
        groups = self.lp_client.get_group_data()
        for group in groups:
            print group.as_dict()
        return True
