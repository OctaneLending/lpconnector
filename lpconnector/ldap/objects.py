import re
from ..config.config import Config


class LDAPObject(object):
    def __init__(self, **kwargs):
        config = Config()
        self.base_dn = config.ldap('BASE_DN')


class LDAPUser(LDAPObject):

    OBJECT_CLASS = "inetOrgPerson"
    ATTRIBUTES = ["uid", "mail", "cn", "memberOf"]

    def __init__(self, **kwargs):
        super(LDAPUser, self).__init__(**kwargs)
        self.uid = kwargs.get('uid')[0]
        self.email = kwargs.get('mail')[0]
        self.name = kwargs.get('cn')[0]
        group_list = []
        for group_dn in kwargs.get('memberOf'):
            group_cn = re.match("cn=(.*),ou", group_dn)
            if group_cn:
                group_list.append(group_cn.group(1))
        self.groups = group_list

    def get_dn(self):
        return "uid=" + self.uid + "," + self.base_dn

    def is_group_member(self, group):
        if isinstance(group, basestring):
            return group in self.groups

        if isinstance(group, object):
            try:
                return group.name in self.groups
            except AttributeError:
                return False

        return False


class LDAPGroup(LDAPObject):

    OBJECT_CLASS = "groupOfNames"
    ATTRIBUTES = ["cn", "member"]

    def __init__(self, **kwargs):
        super(LDAPGroup, self).__init__(**kwargs)
        self.name = kwargs.get('cn')
        member_list = []
        for user_dn in kwargs.get('member'):
            uid = re.match(r"uid=(\w*),ou", user_dn)
            if uid:
                member_list.append(uid.group(1))
        self.members = member_list
        self.member_count = len(self.members)

    def get_dn(self):
        return "cn=" + self.name + "," + self.base_dn

    def is_member(self, user):
        if isinstance(user, basestring):
            return user in self.members

        if isinstance(user, object):
            try:
                return user.uid in self.members
            except AttributeError:
                pass

            try:
                return user.get_uid() in self.members
            except AttributeError:
                pass

        return False
