import requests,sys,traceback
from distutils.util import strtobool
from .user import LastPassUser


class LastPassClient(object):

    url = "https://lastpass.com/enterpriseapi.php"

    def __init__(self, config):
        self.dryRun = strtobool(config.get('ARGS', 'dry-run'))
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
        return self.makeRequest(self.url, payload)

    def postData(self, payload):
        if self.dryRun:
            print payload
            return True
        result = self.makeRequest(self.url, payload)
        return len(result) > 0

    def makeRequest(self, url, payload):
        response = requests.post(url, json=payload)
        try:
            jsonResponse = response.json()
            if 'status' in jsonResponse:
                status = jsonResponse.get('status')
                if status == 'OK':
                    del jsonResponse['status']
                    return jsonResponse
                errors = ""
                if 'error' in jsonResponse:
                    errors = ", ".join(jsonResponse.get('error'))
                elif 'errors' in jsonResponse:
                    errors = ", ".join(jsonResponse.get('errors'))
                else:
                    errors = "No Errors"
                print status + ": " + errors
                return {}
            else:
                return jsonResponse
        except Exception:
            sys.exit("FAIL: Authorization Error; API Connection failed; exiting")
        return {}

