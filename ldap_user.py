import re

class LDAPUser(object):

    objectClass = "inetOrgPerson"
    attributes = ["uid", "mail", "cn", "memberOf"]

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid')[0]
        self.email = kwargs.get('mail')[0]
        self.name = kwargs.get('cn')[0]
        groupList = []
        for dn in kwargs.get('memberOf'):
            cn = re.match("cn=(.*),ou", dn)
            if cn:
                groupList.append(cn.group(1))
        self.groups = groupList

    def __str__(self):
        return "uid=\"%s\",mail=\"%s\",cn=\"%s\"" % (self.uid, self.email, self.name)

    def getJson(self):
        json = "{\"username\":\"" + self.email + "\",\"fullname\":\"" + self.name + "\",\"groups\":["
        for index, group in enumerate(self.groups):
            if index == 0:
                json += "\""+ group + "\""
            else:
                json += ",\""+group + "\""
        json += "],\"attribs\":{\"uid\":\"" + self.uid + "\"}}"
        return json
