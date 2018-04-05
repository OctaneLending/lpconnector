from ..base.objects import BaseUser, BaseObject


class LastPassUser(BaseUser):

    def __init__(self, **kwargs):
        super(LastPassUser, self).__init__(**kwargs)
        self.name = kwargs.get('username')
        self.fullname = kwargs.get('fullname')
        self.groups = kwargs.get('groups')
        self.attribs = kwargs.get('attribs')

    def get_uid(self):
        return self.attribs.get('uid')

    def get_email(self):
        return self.name


class LastPassGroup(BaseObject):

    def __init__(self, **kwargs):
        super(LastPassGroup, self).__init__(**kwargs)
        self.name = kwargs.get('name')
        self.users = kwargs.get('users')

    def is_member(self, user):
        if isinstance(user, str):
            return user in self.users

        if isinstance(user, BaseUser):
            return user.get_email() in self.users

        return False

    def get_count(self):
        return len(self.users)
