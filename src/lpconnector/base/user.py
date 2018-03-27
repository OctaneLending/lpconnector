class BaseUser(object):

    def __init__(self):
        self.groups = []

    def is_group_member(self, group):
        if isinstance(group, basestring):
            return group in self.groups

        if isinstance(group, object):
            try:
                return group.name in self.groups
            except AttributeError:
                return False

        return False

    def get_uid(self):
        raise NotImplementedError

    def get_email(self):
        raise NotImplementedError
