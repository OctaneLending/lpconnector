import requests,os,json

class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self, cid = None, user = None, key = None):
        self.cid = cid if cid else os.getenv('LASTPASS_API_CID')
        self.user = user if user else os.getenv('LASTPASS_API_USER')
        self.basePayload = "{\"cid\":%s,\"provhash\":\"%s\",\"apiuser\":\"%s\",\"cmd\":\"" % (self.cid, self.key, self.user)

    def batchAdd(self, users, defaultPwd = None, pwdReset = True):
        cmd = "batchadd"
        payload = self.basePayload + cmd + "\",\"data\":["
        for index, user in enumerate(users):
            if index == 0 and user:
                payload += user.getJson()
            else:
                payload += "," + user.getJson()

            if defaultPwd is not None:
                payload = payload[:-1]
                payload += ",\"password\":\"" + defaultPwd + "\""
                if not pwdReset:
                    payload += ",\"password_reset_required\":false}"
                else:
                    payload += "}"

        payload += "]}"
        try:
            json.loads(payload)
            print payload
        except ValueError, error:
            print "ERROR: " + error
        # TODO send the request

    def getUserData(self, user = None, disabled = None, admin = None):
        cmd = "getuserdata"
        payload = self.basePayload + cmd + "\""
        dataPayload = False
        if user or disabled is not None  or admin is not None:
            payload += ",\"data\":{"
            if user:
                payload += "\"username\":\"" + user + "\""
                dataPayload = True
            if disabled is not None:
                if dataPayload:
                    payload += ","
                payload += "\"disabled\":" + str(disabled)
                dataPayload = True
            if admin is not None:
                if dataPayload:
                    payload += ","
                payload += "\"admin\":" + str(admin)

            payload += "}"
        payload += "}"
        try:
            json.loads(payload)
            print payload
        except ValueError, error:
            print "ERROR: " + error

        response = requests.post(self.url, json=payload)
        print response
