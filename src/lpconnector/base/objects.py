class BaseObject(object):

    def as_dict(self):
        return self.__dict__


class BaseUser(BaseObject):

    def __init__(self, **kwargs):
        self._raw = kwargs
        self.groups = []

    def __getattr__(self, item):
        if item in self._raw:
            return self._raw.get(item)
        else:
            raise AttributeError

    def is_group_member(self, group):
        if isinstance(group, basestring):
            return group in self.groups

        if isinstance(group, object):
            try:
                return group.name in self.groups
            except AttributeError:
                return False

        return False

    def as_dict(self):
        user_dict = super(BaseUser, self).as_dict()
        del user_dict['_raw']
        return user_dict

    def get_uid(self):
        raise NotImplementedError

    def get_email(self):
        raise NotImplementedError
