from .basecommand import BaseCommand


class Config(BaseCommand):
    """
    Display configuration settings

    Usage:
        lpconnector config

    """

    def execute(self):
        for section in self.config.sections():
            print section + " configs:"
            print dict(self.config.items(section))
        return True
