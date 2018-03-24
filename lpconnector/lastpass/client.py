import sys
import requests
from .user import LastPassUser
from .group import LastPassGroup


class AuthorizationError(Exception):
    pass


class LastPassClient(object):

    DEFAULT_ENDPOINT = "https://lastpass.com/enterpriseapi.php"

    CMD_BATCH_ADD = "batchadd"
    CMD_GET_USER_DATA = "getuserdata"
    CMD_DELETE_USER = "deluser"
    CMD_SYNC_GROUPS = "batchchangegrp"

    def __init__(self, cid, user, key, dry_run, url = None):
        self.url = url if url is not None else LastPassClient.DEFAULT_ENDPOINT
        self.dry_run = dry_run
        self.cid = cid
        self.user = user
        self.key = key

    def build_payload(self, command, data=None, **kwargs):
        data_payload = {}

        if data:
            data_payload.update(data)

        if kwargs:
            data_payload.update(kwargs)

        base_payload = {
            "cid": self.cid,
            "provhash": self.key,
            "apiuser": self.user,
            "cmd": command,
        }

        if len(data_payload) > 0:
            base_payload.update(data=data_payload)

        return base_payload

    def batch_add(self, users, default_pwd = None, pwd_reset = None):
        user_data = []

        for user in users:
            user_payload = user.getLastPassUser().__dict__

            if default_pwd is not None:
                user_payload['password'] = defaultpwd
                if pwd_reset is not None:
                    user_payload['password_reset_required'] = pwd_reset

            user_data.append(user_payload)

        return self.post_data(LastPassClient.CMD_BATCH_ADD, user_data)

    def get_user_data(self, user=None, disabled=None, admin=None):
        data_payload = {}
        if user is not None or disabled or admin:
            if user is not None:
                data_payload['username'] = user
            if disabled:
                data_payload['disabled'] = 1
            if admin:
                data_payload['admin'] = 1

        users = []
        response = self.get_data(
            command=LastPassClient.CMD_GET_USER_DATA,
            data_payload=data_payload
        )
        if response:
            for user in response.get('Users').values():
                users.append(LastPassUser(**user))
        return users

    def get_group_data(self):
        response = self.get_data(LastPassClient.CMD_GET_USER_DATA)
        groups = []
        if response:
            for group, users in response.get('Groups').iteritems():
                groups.append(LastPassGroup(name=group, users=users))
        return groups

    def delete_user(self, user, action = 0):
        cmd = "deluser"
        payload = self.basePayload
        payload['cmd'] = cmd
        payload['data'] = {"username": user, "deleteaction": action}
        return self.postData(payload)

    def sync_groups(self, userPayload):
        cmd = "batchchangegrp"
        payload = self.basePayload
        payload['cmd'] = cmd
        payload['data'] = userPayload
        return self.postData(payload)

    def get_data(self, command, data_payload=None):
        payload = self.build_payload(command, data_payload)
        if self.dry_run:
            print payload
            return {}
        return self.make_request(self.url, payload)

    def post_data(self, data_payload=None):
        if self.dryRun:
            print payload
            return True
        result = self.makeRequest(self.url, payload)
        return len(result) > 0

    def make_request(self, url, payload):
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

