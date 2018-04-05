import pytest
from copy import deepcopy
from mock import patch, Mock
from src.lpconnector.base.objects import BaseObject, BaseUser
from src.lpconnector.ldap.objects import LDAPObject, LDAPUser, LDAPGroup, LDAPObjectException
from src.lpconnector.lastpass.objects import LastPassUser, LastPassGroup


TEST_DN = "ou=OU,dc=test,dc=com"


LDAP_USER_RAW = {
    'cn': ['Testy McTester'],
    'mobile': ['5555555555'],
    'memberOf': [
        'cn=Test Group,ou=OU,dc=test,dc=com',
        'cn=Other Test Group,ou=OU,dc=test,dc=com',
    ],
    'uidNumber': ['5555'],
    'objectClass': [
        'top',
        'person',
        'organizationalPerson',
        'inetOrgPerson',
    ],
    'gidNumber': ['5555'],
    'sn': ['McTester'],
    'mail': ['test@test.com'],
    'givenName': ['Testy'],
    'uid': ['testy']
}

LDAP_GROUP_RAW = {
    'objectClass': [
        'top',
        'groupOfNames',
    ],
    'member': [
        'uid=testy,ou=OU,dc=test,dc=com',
        'uid=othertester,ou=OU,dc=test,dc=com',
    ],
    'ou': ['Test Group'],
    'cn': ['Test Group']
}


LP_USER_RAW = {
    'username': 'test@test.com',
    'fullname': 'Testy McTester',
    'attribs': {'uid': 'test'},
    'groups': ['Test Group', 'Other Test Group'],
    'other': 'other',
}

LP_GROUP_RAW = {
    'name': 'Test Group',
    'users': [
        'test@test.com',
        'othertest@test.com',
    ]
}


def test_base_object():
    base_obj_a = BaseObject()
    assert isinstance(base_obj_a, object)
    assert hasattr(base_obj_a, '_raw')
    assert isinstance(base_obj_a._raw, dict)
    assert hasattr(base_obj_a, 'name')
    assert not base_obj_a.name
    assert not base_obj_a.as_dict()
    base_obj_b = BaseObject(**LP_USER_RAW)
    assert hasattr(base_obj_b, 'name')
    assert not base_obj_b.name
    assert not base_obj_b.as_dict()
    base_obj_c = BaseObject(**LP_GROUP_RAW)
    assert hasattr(base_obj_c, 'name')
    assert base_obj_c.name == 'Test Group'
    assert base_obj_c.as_dict() == {'name': 'Test Group'}


def test_base_user_init():
    base_user = BaseUser(**LP_USER_RAW)
    assert hasattr(base_user, '_raw')
    assert isinstance(base_user._raw, dict)
    assert base_user._raw == LP_USER_RAW
    assert hasattr(base_user, 'groups')
    assert isinstance(base_user.groups, list)
    assert base_user.groups == LP_USER_RAW.get('groups')


def test_base_user_methods():
    base_user = BaseUser(**LP_USER_RAW)
    with pytest.raises(NotImplementedError):
        no_uid = base_user.get_uid()
    with pytest.raises(NotImplementedError):
        no_email = base_user.get_email()
    base_obj = BaseObject(**LP_GROUP_RAW)
    assert base_user.is_group_member('Test Group')
    assert base_user.is_group_member(base_obj)
    assert not base_user.is_group_member('Not Test Group')
    assert not base_user.is_group_member(1)
    del base_obj.name
    assert not base_user.is_group_member(base_obj)


@patch('src.lpconnector.ldap.objects.BaseConfig')
def test_ldap_object(mock_base_config):
    mock_base_config.return_value.ldap.return_value = TEST_DN
    ldap_obj = LDAPObject(**LDAP_GROUP_RAW)
    assert ldap_obj._base_dn == TEST_DN
    assert '_base_dn' not in ldap_obj.as_dict()
    with pytest.raises(NotImplementedError):
        no_dn = ldap_obj.get_dn()
    no_obj_class = deepcopy(LDAP_GROUP_RAW)
    del no_obj_class['objectClass']
    with pytest.raises(LDAPObjectException):
        no_ldap_obj = LDAPObject(**no_obj_class)


@patch('src.lpconnector.ldap.objects.BaseConfig')
@patch('src.lpconnector.ldap.objects.LDAPUser.ATTRIBUTES_MAP', {
    'uid': 'uid',
    'mail': 'email',
    'cn': 'name',
    'memberOf': 'groups',
    'objectClass': 'classes'
})
def test_ldap_user(mock_base_config):
    mock_base_config.return_value.ldap.return_value = TEST_DN
    ldap_user = LDAPUser(**LDAP_USER_RAW)
    for attr in LDAPUser.ATTRIBUTES_MAP.values():
        assert hasattr(ldap_user, attr)
    assert isinstance(ldap_user.groups, list)
    assert len(ldap_user.groups) == len(LDAP_USER_RAW.get('memberOf'))
    assert ldap_user.get_uid() == LDAP_USER_RAW.get('uid')[0]
    assert ldap_user.get_email() == LDAP_USER_RAW.get('mail')[0]
    assert ldap_user.get_dn() == "uid=" + LDAP_USER_RAW.get('uid')[0] + "," + TEST_DN
    bad_obj_class = deepcopy(LDAP_USER_RAW)
    bad_obj_class.get('objectClass').remove(LDAPUser.OBJECT_CLASS)
    with pytest.raises(LDAPObjectException):
        no_ldap_user = LDAPUser(**bad_obj_class)


@patch('src.lpconnector.ldap.objects.BaseConfig')
@patch('src.lpconnector.ldap.objects.LDAPGroup.ATTRIBUTES_MAP', {
    'cn': 'name',
    'member': 'members',
    'objectClass': 'classes'
})
def test_ldap_group(mock_base_config):
    mock_base_config.return_value.ldap.return_value = TEST_DN
    ldap_group = LDAPGroup(**LDAP_GROUP_RAW)
    for attr in LDAPGroup.ATTRIBUTES_MAP.values():
        assert hasattr(ldap_group, attr)
    assert isinstance(ldap_group.members, list)
    assert ldap_group.name == LDAP_GROUP_RAW.get('cn')[0]
    assert ldap_group.get_count() == len(LDAP_GROUP_RAW.get('member'))
    assert ldap_group.get_dn() == "cn=" + LDAP_GROUP_RAW.get('cn')[0] + "," + TEST_DN
    ldap_user = LDAPUser(**LDAP_USER_RAW)
    assert ldap_group.is_member(ldap_user)
    assert ldap_group.is_member('othertester')
    assert not ldap_group.is_member('nottest')
    assert not ldap_group.is_member(1)
    bad_obj_class = deepcopy(LDAP_GROUP_RAW)
    bad_obj_class.get('objectClass').remove(LDAPGroup.OBJECT_CLASS)
    with pytest.raises(LDAPObjectException):
        no_ldap_group = LDAPGroup(**bad_obj_class)


def test_lastpass_user_init():
    lp_user = LastPassUser(**LP_USER_RAW)
    assert hasattr(lp_user, 'name')
    assert isinstance(lp_user.name, str)
    assert hasattr(lp_user, 'fullname')
    assert isinstance(lp_user.fullname, str)
    assert hasattr(lp_user, 'attribs')
    assert isinstance(lp_user.attribs, dict)
    assert hasattr(lp_user, 'groups')
    assert isinstance(lp_user.groups, list)
    assert hasattr(lp_user, '_raw')
    assert hasattr(lp_user, 'other')
    assert not hasattr(lp_user, 'another')
    with pytest.raises(AttributeError):
        var = lp_user.another


def test_lastpass_user_methods():
    lp_user = LastPassUser(**LP_USER_RAW)
    assert lp_user.get_uid() == LP_USER_RAW.get('attribs').get('uid')
    assert lp_user.get_email() == LP_USER_RAW.get('username')
    assert lp_user.is_group_member('Test Group')
    assert not lp_user.is_group_member('Not Test Group')
    lp_user_expected = deepcopy(LP_USER_RAW)
    del lp_user_expected['other']
    lp_user_expected['name'] = lp_user_expected.pop('username')
    assert lp_user.as_dict() == lp_user_expected


def test_lastpass_group_init():
    lp_group = LastPassGroup(**LP_GROUP_RAW)
    assert hasattr(lp_group, 'name')
    assert isinstance(lp_group.name, str)
    assert lp_group.name == LP_GROUP_RAW.get('name')
    assert hasattr(lp_group, 'users')
    assert isinstance(lp_group.users, list)
    assert lp_group.users == LP_GROUP_RAW.get('users')


def test_lastpass_group_methods():
    lp_group = LastPassGroup(**LP_GROUP_RAW)
    assert lp_group.as_dict() == LP_GROUP_RAW
    assert lp_group.get_count() == len(LP_GROUP_RAW.get('users'))
    lp_user = LastPassUser(**LP_USER_RAW)
    assert lp_group.is_member(lp_user)
    assert lp_group.is_member('othertest@test.com')
    assert not lp_group.is_member('someone@test.com')
    assert not lp_group.is_member(1)
