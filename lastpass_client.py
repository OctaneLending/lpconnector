import requests,os,json

class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self, cid = None, user = None, key = None):
        self.cid = cid if cid else os.getenv('LASTPASS_API_CID')
        self.user = user if user else os.getenv('LASTPASS_API_USER')
        self.key = ley if key else os.getenv('LASTPASS_API_SECRET')
        self.basePayload = {
            "cid": self.cid,
            "provhash": self.key,
            "apiuser": self.user,
            "cmd": ""
        }

    def batchAdd(self, users, defaultPwd = None, pwdReset = None):
        cmd = "batchadd"
        payload = self.basePayload
        payload['cmd'] = cmd
        payload['data'] = []
        for user in users:
            userPayload = user.__dict__
            if defaultPwd is not None:
                userPayload['password'] = defaultPwd
                if pwdReset is not None:
                    userPayload['password_reset_required'] = pwdReset
            payload['data'].append(userPayload)
        try:
            jsonPayload = json.dumps(payload)
            json.loads(jsonPayload)
            print jsonPayload
        except ValueError, error:
            print "ERROR: " + error
        # TODO send the request

    def getUserData(self, user = None, disabled = None, admin = None):
        cmd = "getuserdata"
        payload = self.basePayload
        payload['cmd'] = cmd
        if user or disabled is not None  or admin is not None:
            dataPayload = {}
            if user:
                dataPayload['username'] = user
            if disabled is not None:
                dataPayload['disabled'] = str(disabled)
            if admin is not None:
                dataPayload['admin'] = str(admin)
            payload['data'] = dataPayload
        try:
            jsonPayload = json.dumps(payload)
            json.loads(jsonPayload)
            print jsonPayload
        except ValueError, error:
            print "ERROR: " + error

        response = requests.post(self.url, json=jsonPayload)
        print response
