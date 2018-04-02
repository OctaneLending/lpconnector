import re
from ..base.user import BaseUser
from ..base.config import BaseConfig


class LDAPObject(object):
    def __init__(self):
        config = BaseConfig()
        self.base_dn = config.ldap('BASE_DN')

    def as_dict(self):
        obj_dict = self.__dict__
        del obj_dict['base_dn']
        return obj_dict

    def get_dn(self):
        raise NotImplementedError


class LDAPUser(LDAPObject, BaseUser):

    OBJECT_CLASS = "inetOrgPerson"
    ATTRIBUTES = ["uid", "mail", "cn", "memberOf"]

    def __init__(self, **kwargs):
        super(LDAPUser, self).__init__()
        self.uid = kwargs.get('uid')[0]
        self.email = kwargs.get('mail')[0]
        self.name = kwargs.get('cn')[0]
        group_list = []
        for group_dn in kwargs.get('memberOf'):
            group_cn = re.match("cn=(.*),ou", group_dn)
            if group_cn:
                group_list.append(group_cn.group(1))
        self.groups = group_list

    def get_uid(self):
        return self.uid

    def get_email(self):
        return self.email

    def get_dn(self):
        return "uid=" + self.uid + "," + self.base_dn


class LDAPGroup(LDAPObject):

    OBJECT_CLASS = "groupOfNames"
    ATTRIBUTES = ["cn", "member"]

    def __init__(self, **kwargs):
        super(LDAPGroup, self).__init__()
        self.name = kwargs.get('cn')
        member_list = []
        for user_dn in kwargs.get('member'):
            uid = re.match(r"uid=(\w*),ou", user_dn)
            if uid:
                member_list.append(uid.group(1))
        self.members = member_list

    def get_dn(self):
        return "cn=" + self.name + "," + self.base_dn

    def get_count(self):
        return len(self.members)

    def is_member(self, user):
        if isinstance(user, basestring):
            return user in self.members

        if isinstance(user, BaseUser):
            return user.get_uid() in self.members

        return False
