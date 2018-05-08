from __future__ import print_function
import sys
from time import sleep
import requests
from ..ldap.objects import LDAPUser
from .objects import LastPassUser, LastPassGroup
from ..base import print_error


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
        self.key = config.get('api_provhash')

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

    def batch_add(self, users, throttle=0, default_pwd=None, pwd_reset=None):
        user_data = []

        if throttle > 0:
            count = 0
            for user in users:
                lp_user = self.ldap_to_lastpass_user(user)
                if isinstance(lp_user, LastPassUser):
                    user_payload = self.ldap_to_lastpass_user(user).as_dict()
                    user_payload['username'] = user_payload.pop('name')

                    if default_pwd is not None:
                        user_payload['password'] = default_pwd
                        if pwd_reset is not None:
                            user_payload['password_reset_required'] = pwd_reset

                    user_data.append(user_payload)
                    count += 1

                if count == throttle:
                    print('Provisioning ' + str(count) + ' users...')
                    self.post_data(LastPassClient.CMD_BATCH_ADD, user_data)
                    count = 0
                    user_data = []
                    sleep(1)
            # Any users left over
            if count > 0:
                print('Provisioning ' + str(count) + ' users...')
                self.post_data(LastPassClient.CMD_BATCH_ADD, user_data)

        else:
            for user in users:
                lp_user = self.ldap_to_lastpass_user(user)
                if isinstance(lp_user, LastPassUser):
                    user_payload = self.ldap_to_lastpass_user(user).as_dict()
                    user_payload['username'] = user_payload.pop('name')

                    if default_pwd is not None:
                        user_payload['password'] = default_pwd
                        if pwd_reset is not None:
                            user_payload['password_reset_required'] = pwd_reset

                    user_data.append(user_payload)

        return self.post_data(LastPassClient.CMD_BATCH_ADD, user_data)

    def get_user_data(self, user=None, disabled=None, admin=None):
        data_payload = {}

        if user is not None:
            data_payload['username'] = user
        if disabled is not None:
            data_payload['disabled'] = int(disabled)
        if admin is not None:
            data_payload['admin'] = int(admin)

        users = []
        response = self.get_data(
            command=LastPassClient.CMD_GET_USER_DATA,
            data_payload=data_payload
        )
        if 'Users' in response:
            for lp_user in response.get('Users').values():
                users.append(LastPassUser(**lp_user))
        else:
            print('User(s) not found')
        return users

    def get_group_data(self):
        response = self.get_data(LastPassClient.CMD_GET_USER_DATA)
        groups = []
        if 'Groups' in response:
            for group in response.get('Groups').values():
                groups.append(LastPassGroup(**group))
        else:
            print('Group(s) not found')
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
        return self.make_request(self.url, payload)

    def post_data(self, command, data_payload=None):
        payload = self.build_payload(command, data_payload)
        if self.dry_run:
            print(payload)
            return True
        result = self.make_request(self.url, payload)

        if 'status' in result:
            status = result.get('status')
            errors = "No Errors"
            if status == 'OK':
                del result['status']
                if 'message' in result:
                    print(result.get('message'))
                    print('Consider throttling your provisioning')
                return True
            if 'error' in result:
                errors = ", ".join(result.get('error'))
            elif 'errors' in result:
                errors = ", ".join(result.get('errors'))
            print(status + ": " + errors)
            return False

        return False

    @staticmethod
    def make_request(url, payload):
        try:
            response = requests.post(url, json=payload)
        except requests.exceptions.RequestException as error:
            print_error('FAIL: {0}; {1}'.format(type(error).__name__, str(error)))
            sys.exit('LastPass API connection failed; exiting')

        # If there is an authorization error, the LastPass API will return a 200 but with
        # an XML body, so .json() will throw an exception when trying to decode
        try:
            json_response = response.json()
        except ValueError:
            print_error('FAIL: AuthorizationError; Invalid provhash or cid')
            sys.exit('LastPass API connection failed; exiting')
        return json_response
