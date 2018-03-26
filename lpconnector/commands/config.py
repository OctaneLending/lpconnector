from .basecommand import BaseCommand


class Config(BaseCommand):
    """
    Display configuration settings

    Usage:
        lpconnector config

    """

    def execute(self):
        for section in self.config.section_names():
            print section + " configs:"
            print dict(self.config.get_section(section))
        return True
