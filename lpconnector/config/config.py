import os
import ConfigParser


class Config(object):

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.abspath('lpconnector'), 'config/config.ini')

        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path)

    def section_names(self):
        return self.config.sections()

    def get_section(self, section):
        return self.config.items(section)

    def get_value(self, section, key):
        return self.config.get(section, key)

    def ldap(self, key=None):
        if key is None:
            return self.get_section('LDAP')
        return self.get_value('LDAP', key)

    def lastpass(self, key=None):
        if key is None:
            return self.get_section('LASTPASS')
        return self.get_value('LASTPASS', key)
