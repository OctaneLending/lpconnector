import pytest
from src.lpconnector.base.objects import BaseObject, BaseUser
from src.lpconnector.ldap.objects import LDAPObject, LDAPUser, LDAPGroup
from src.lpconnector.lastpass.objects import LastPassUser, LastPassGroup




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
    assert base_user.groups == []


def test_base_user_methods():
    base_user = BaseUser(**LP_USER_RAW)
    assert base_user.username == LP_USER_RAW.get('username')
    with pytest.raises(AttributeError):
        var = base_user.nothing


def test_lastpass_user_init():
    lp_user = LastPassUser(**LP_USER_RAW)
    assert hasattr(lp_user, 'username')
    assert isinstance(lp_user.username, str)
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
    lp_user_expected = LP_USER_RAW
    del lp_user_expected['other']
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