import re

class LDAPGroup(object):

    objectClass = "groupOfNames"
    attributes = ["cn", "member"]

    def __init__(self, **kwargs):
        self.name = kwargs.get('cn')
        memberList = []
        for dn in kwargs.get('member'):
            uid = re.match("uid=(\w*),ou", dn)
            if uid:
                memberList.append(uid.group(1))
        self.members = memberList
