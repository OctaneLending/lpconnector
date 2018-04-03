class BaseObject(object):

    def __init__(self, **kwargs):
        self.name = None
        if 'name' in kwargs:
            self.name = kwargs.get('name')

    def as_dict(self):
        obj_dict = self.__dict__
        if hasattr(self, 'name') and not self.name:
            del obj_dict['name']
        return obj_dict


class BaseUser(BaseObject):

    def __init__(self, **kwargs):
        super(BaseUser, self).__init__(**kwargs)
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

        if isinstance(group, BaseObject):
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
