from __future__ import print_function
import requests
from ..ldap.objects import LDAPUser
from .objects import LastPassUser, LastPassGroup


class AuthorizationError(Exception):
    pass


class LastPassClient(object):

    DEFAULT_ENDPOINT = "https://lastpass.com/enterpriseapi.php"

    CMD_BATCH_ADD = "batchadd"
    CMD_GET_USER_DATA = "getuserdata"
    CMD_DELETE_USER = "deluser"
    CMD_SYNC_GROUPS = "batchchangegrp"

    def __init__(self, dry_run, url, **kwargs):
        config = dict(kwargs.get('config'))
        self.dry_run = dry_run
        self.url = url
        self.cid = config.get('api_cid')
        self.user = config.get('api_user')
        self.key = config.get('api_secret')

    @staticmethod
    def ldap_to_lastpass_user(user):
        if isinstance(user, LDAPUser):
            return LastPassUser(
                username=user.get_email(),
                fullname=user.name,
                groups=user.groups,
                attribs={'uid': user.get_uid()}
            )
        return None

    def build_payload(self, command, data=None):
        payload = {
            "cid": self.cid,
            "provhash": self.key,
            "apiuser": self.user,
            "cmd": command,
        }
        if data is not None:
            payload.update(data=data)

        return payload

    def batch_add(self, users, default_pwd=None, pwd_reset=None):
        user_data = []

        for user in users:
            lp_user = self.ldap_to_lastpass_user(user)
            if isinstance(lp_user, LastPassUser):
                user_payload = self.ldap_to_lastpass_user(user).as_dict()

                if default_pwd is not None:
                    user_payload['password'] = default_pwd
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
            for lp_user in response.get('Users').values():
                users.append(LastPassUser(**lp_user))
        return users

    def get_group_data(self):
        response = self.get_data(LastPassClient.CMD_GET_USER_DATA)
        groups = []
        if response:
            for group in response.get('Groups').values():
                groups.append(LastPassGroup(**group))
        return groups

    def delete_user(self, user, action=0):
        return self.post_data(
            command=LastPassClient.CMD_DELETE_USER,
            data_payload={'username': user, 'deleteaction': action}
        )

    def sync_groups(self, user_payload):
        return self.post_data(
            command=LastPassClient.CMD_SYNC_GROUPS,
            data_payload=user_payload
        )

    def get_data(self, command, data_payload=None):
        payload = self.build_payload(command, data_payload)
        if self.dry_run:
            print(payload)
            return {}
        return self.make_request(self.url, payload)

    def post_data(self, command, data_payload=None):
        payload = self.build_payload(command, data_payload)
        if self.dry_run:
            print(payload)
            return True
        result = self.make_request(self.url, payload)
        return len(result) > 0

    @staticmethod
    def make_request(url, payload):
        response = requests.post(url, json=payload)
        try:
            json_response = response.json()
            if 'status' in json_response:
                status = json_response.get('status')
                errors = "No Errors"
                if status == 'OK':
                    del json_response['status']
                    return json_response
                if 'error' in json_response:
                    errors = ", ".join(json_response.get('error'))
                elif 'errors' in json_response:
                    errors = ", ".join(json_response.get('errors'))
                print(status + ": " + errors)
                return {}

        except Exception:
            print("FAIL: Authorization Error; API Connection failed; exiting")
            raise AuthorizationError(Exception)
        return json_response
