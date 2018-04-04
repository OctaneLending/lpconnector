import re
from ..base.objects import BaseUser, BaseObject
from ..base.config import BaseConfig


class LDAPObjectException(Exception):
    pass


class LDAPObject(BaseObject):
    def __init__(self, **kwargs):
        print kwargs
        if 'objectClass' not in kwargs:
            raise LDAPObjectException('LDAP Object has no object class')

        super(LDAPObject, self).__init__(**kwargs)

        self._base_dn = BaseConfig().ldap('BASE_DN')

    def as_dict(self):
        obj_dict = super(LDAPObject, self).as_dict()
        del obj_dict['_base_dn']
        return obj_dict

    def get_dn(self):
        raise NotImplementedError


class LDAPUser(BaseUser, LDAPObject):

    # Object class that identifies a user
    OBJECT_CLASS = "inetOrgPerson"
    # LDAP attributes to store as class attributes
    # uid, mail, and memberOf are mandatory
    ATTRIBUTES_MAP = {
        'uid': 'uid',
        'mail': 'email',
        'cn': 'name',
        'memberOf': 'groups'
    }
    # Filter out groups that contain non-employee accounts
    NON_USER_GROUPS = ['Service Accounts']

    def __init__(self, **kwargs):
        super(LDAPUser, self).__init__(**kwargs)

        if self.OBJECT_CLASS not in kwargs.get('objectClass'):
            raise LDAPObjectException('LDAP Object is not an LDAP user')

        # Mandatory Attributes
        self.uid = ""
        self.email = ""

        for attr, param in self.ATTRIBUTES_MAP.items():
            ldap_attr = kwargs.get(attr)
            if attr == 'memberOf':
                group_list = []
                for group_dn in ldap_attr:
                    group_cn = re.match("cn=(.*),ou", group_dn)
                    if group_cn:
                        group_list.append(group_cn.group(1))
                setattr(self, param, group_list)
            elif attr == 'objectClass':
                setattr(self, param, ldap_attr)
            else:
                setattr(self, param, ldap_attr[0])

    def get_uid(self):
        return self.uid

    def get_email(self):
        return self.email

    def get_dn(self):
        return "uid=" + self.uid + "," + self._base_dn


class LDAPGroup(LDAPObject):

    # Object class that identifies a user
    OBJECT_CLASS = "groupOfNames"
    # LDAP attributes to store as class attributes
    # cn and member are mandatory
    ATTRIBUTES_MAP = {
        'cn': 'name',
        'member': 'members'
    }

    def __init__(self, **kwargs):
        super(LDAPGroup, self).__init__(**kwargs)

        if self.OBJECT_CLASS not in kwargs.get('objectClass'):
            raise LDAPObjectException('LDAP Object is not an LDAP group')

        # Mandatory Attributes
        self.name = ""
        self.members = []

        for attr, param in self.ATTRIBUTES_MAP.items():
            ldap_attr = kwargs.get(attr)
            if attr == 'member':
                member_list = []
                for user_dn in ldap_attr:
                    uid = re.match(r"uid=(\w*),ou", user_dn)
                    if uid:
                        member_list.append(uid.group(1))
                setattr(self, param, member_list)
            elif attr == 'objectClass':
                setattr(self, param, ldap_attr)
            else:
                setattr(self, param, ldap_attr[0])

    def get_dn(self):
        return "cn=" + self.name + "," + self._base_dn

    def get_count(self):
        return len(self.members)

    def is_member(self, user):
        if isinstance(user, basestring):
            return user in self.members

        if isinstance(user, BaseUser):
            return user.get_uid() in self.members

        return False
