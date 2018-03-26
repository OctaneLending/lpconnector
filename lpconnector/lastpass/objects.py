class LastPassUser(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.fullname = kwargs.get('fullname')
        self.groups = kwargs.get('groups')
        self.attribs = kwargs.get('attribs')

    def get_uid(self):
        return self.attribs.get('uid')

    def is_group_member(self, group):
        if isinstance(group, basestring):
            return group in self.groups

        if isinstance(group, object):
            try:
                return group.name in self.groups
            except AttributeError:
                return False

        return False


class LastPassGroup(object):

    def __init__(self, name, users):
        self.name = name
        self.users = users

    def is_member(self, user):
        if isinstance(user, basestring):
            return user in self.users

        if isinstance(user, object):
            try:
                return user.email in self.members
            except AttributeError:
                pass

            try:
                return user.username in self.members
            except AttributeError:
                pass

        return False
