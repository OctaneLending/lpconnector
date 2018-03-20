import requests,os,json
from .user import LastPassUser

class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self, config):
        self.cid = config.get('LASTPASS', 'API_CID')
        self.user = config.get('LASTPASS', 'API_USER')
        self.key = config.get('LASTPASS', 'API_SECRET')
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
            userPayload = user.getLastPassUser().__dict__
            if defaultPwd is not None:
                userPayload['password'] = defaultPwd
                if pwdReset is not None:
                    userPayload['password_reset_required'] = pwdReset
            payload['data'].append(userPayload)

        response = requests.post(self.url, json=payload)
        return response

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

        users = []
        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            print "Error getting LastPass Users"
        else:
            jsonResponse = response.json()
            print jsonResponse.get('status')
            if jsonResponse.get('status') in ['WARN', 'FAIL']:
                print "Could not find user: " + user
            else:
                jsonReturn = response.json().get('Users')
                for user in jsonReturn.values():
                    users.append(LastPassUser(**user))

        return users
