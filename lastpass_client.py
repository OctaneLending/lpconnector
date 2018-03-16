import requests,os,json

class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self):
        self.cid = os.getenv('LASTPASS_API_CID')
        self.user = os.getenv('LASTPASS_API_USER')
        self.key = os.getenv('LASTPASS_API_SECRET')

    def batchAdd(self, users, defaultPwd = None, pwdReset = True):
        cmd = "batchadd"
        payload = "{\"cid\":%s,\"provhash\":\"%s\",\"apiuser\":\"%s\",\"cmd\":\"%s\",\"data\":[" % (self.cid, self.key, self.user, cmd)
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
        print payload
        try:
            json.loads(payload)
        except ValueError, error:
            print "ERROR: " + error
        # TODO send the request

