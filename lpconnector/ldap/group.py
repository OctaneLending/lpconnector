import re


class LDAPGroup(object):

    OBJECT_CLASS = "groupOfNames"
    ATTRIBUTES = ["cn", "member"]

    def __init__(self, **kwargs):
        self.name = kwargs.get('cn')
        member_list = []
        for user_dn in kwargs.get('member'):
            uid = re.match(r"uid=(\w*),ou", user_dn)
            if uid:
                member_list.append(uid.group(1))
        self.members = member_list
        self.member_count = len(self.members)
