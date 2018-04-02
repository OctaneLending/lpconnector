import pytest
from src.lpconnector.lastpass.objects import LastPassUser


LP_USER_RAW = {
    'username': 'test@test.com',
    'fullname': 'Testy McTester',
    'attribs': {'uid': 'test'},
    'groups': ['Test Group', 'Other Test Group'],
    'other': 'other',
}


@pytest.mark.timeout(60)
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
        lp_user.another


def test_lastpass_user_methods():
    lp_user = LastPassUser(**LP_USER_RAW)
    assert lp_user.get_uid() == LP_USER_RAW.get('attribs').get('uid')
    assert lp_user.get_email() == LP_USER_RAW.get('username')
    assert lp_user.is_group_member('Test Group')
    assert not lp_user.is_group_member('Not Test Group')
    lp_user_expected = LP_USER_RAW
    del lp_user_expected['other']
    assert lp_user.as_dict() == lp_user_expected
