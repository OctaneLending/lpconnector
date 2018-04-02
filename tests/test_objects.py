import pytest
from src.lpconnector.ldap.objects import LDAPObject, LDAPUser, LDAPGroup
from src.lpconnector.lastpass.objects import LastPassUser, LastPassGroup


lp_user_raw = {
    'username': 'test@test.com',
    'fullname': 'Testy McTester',
    'attribs': {'uid': 'test'},
    'groups': ['Test Group', 'Other Test Group'],
    'other': 'other'
}


def test_lastpass_user_init():
    lp_user = LastPassUser(**lp_user_raw)
    assert hasattr(lp_user, 'username')
    assert isinstance(lp_user.username, str)
    assert hasattr(lp_user, 'fullname')
    assert isinstance(lp_user.fullname, str)
    assert hasattr(lp_user, 'attribs')
    assert isinstance(lp_user.attribs, dict)
    assert hasattr(lp_user, 'groups')
    assert isinstance(lp_user.groups, list)
    assert not hasattr(lp_user, '__raw')
    assert hasattr(lp_user, '_LastPassUser__raw')
    assert hasattr(lp_user, 'other')
    assert not hasattr(lp_user, 'another')
    #with pytest.raises(AttributeError):
        #lp_user.another


def test_lastpass_user_methods():
    lp_user = LastPassUser(**lp_user_raw)
    assert lp_user.get_uid() == lp_user_raw.get('attribs').get('uid')
    assert lp_user.get_email() == lp_user_raw.get('username')
    assert lp_user.as_dict() != lp_user_raw
    lp_user_expected = lp_user_raw
    del lp_user_expected['other']
    assert lp_user.as_dict() == lp_user_expected
