import os
import ConfigParser


class BaseConfig(object):

    def __init__(self, config_file=None):
        if config_file is None:
            config_file = 'config.ini'
        config_path = os.path.join(os.path.dirname(__file__), 'config/' + config_file)

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
