import requests,sys
from .user import LastPassUser


class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self, config):
        self.dryRun = config.get('ARGS', 'dry-run')
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

        return self.postData(payload)

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
        response = self.getData(payload)
        for user in response.get('Users').values():
            users.append(LastPassUser(**user))
        return users

    def deleteUser(self, user, action = 0):
        cmd = "deluser"
        payload = self.basePayload
        payload['cmd'] = cmd
        payload['data'] = {"username": user, "deleteaction": action}
        return self.postData(payload)

    def syncGroups(self, userPayload):
        cmd = "batchchangegrp"
        payload = self.basePayload
        payload['cmd'] = cmd
        payload['data'] = userPayload
        return self.postData(payload)

    def getData(self, payload):
        if self.dryRun:
            print payload
            return {}
        response = requests.post(self.url, json=payload)
        try:
            jsonResponse = response.json()
            if 'status' in jsonResponse:
                status = jsonResponse.get('status')
                print status + ": " + jsonResponse.get('errors')
                if status == 'FAIL':
                    sys.exit('API connection failed; exiting.')
                return {}
            else:
                return jsonResponse
        except Exception:
            sys.exit("FAIL: Authorization Error; API Connection failed; exiting")
        return {}

    def postData(self, payload):
        if self.dryRun:
            print payload
            return True
        response = requests.post(self.url, json=payload)
        if 'json' in response.headers['Content-Type']:
            jsonResponse = response.json()
            status = jsonResponse.get('status')
            if status != 'OK':
                print status + ": " + jsonResponse.get('errors')
                if status == 'FAIL':
                    sys.exit('API connection failed; exiting.')
                return False
        elif 'xml' in response.headers['Content-Type']:
            sys.exit("FAIL: Authorization Error; API Connection failed; exiting")
        return True

