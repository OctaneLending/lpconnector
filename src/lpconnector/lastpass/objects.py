from ..base.user import BaseUser


class LastPassUser(BaseUser):

    def __init__(self, **kwargs):
        super(LastPassUser, self).__init__()
        self.__raw = kwargs
        self.username = kwargs.get('username')
        self.fullname = kwargs.get('fullname')
        self.groups = kwargs.get('groups')
        self.attribs = kwargs.get('attribs')

    def __getattribute__(self, item):
        if not hasattr(self, item):
            if self.__raw.has_key(item):
                return self.__raw.get(item)
            else:
                raise AttributeError
        else:
            return BaseUser.__getattribute__(self, item)

    def as_dict(self):
        user_dict = self.__dict__
        del user_dict['_LastPassUser__raw']
        return user_dict

    def get_uid(self):
        return self.attribs.get('uid')

    def get_email(self):
        return self.username


class LastPassGroup(object):

    def __init__(self, name, users):
        self.name = name
        self.users = users

    def is_member(self, user):
        if isinstance(user, basestring):
            return user in self.users

        if isinstance(user, BaseUser):
            return user.get_email() in self.users

        return False

    def get_count(self):
        return len(self.users)
