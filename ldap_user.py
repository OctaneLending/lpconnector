import re

class LDAPUser(object):

    objectClass = "inetOrgPerson"
    attributes = ["mail", "cn", "memberOf"]

    def __init__(self, **kwargs):
        self.email = kwargs.get('mail')
        self.name = kwargs.get('cn')
        groupList = []
        for dn in kwargs.get('memberOf'):
            cn = re.match("\cn=(\w*),ou", dn)
            if cn:
                groupList.append(cn.group(1))
        self.groups = groupList
