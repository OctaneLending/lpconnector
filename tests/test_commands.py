import sys
import pytest
import src.lpconnector.commands as commands
from src.lpconnector.ldap.server import LDAPServer
from src.lpconnector.lastpass.client import LastPassClient


def test_base_command_bad_cmd():
    with pytest.raises(Exception):
        commands.BaseCommand('test', {})


def test_base_command_fail_execute():
    base_command = commands.BaseCommand('config', {})
    with pytest.raises(NotImplementedError):
        base_command.execute()


def test_base_command_good_cmd_no_args():
    base_command = commands.BaseCommand('config', {})
    assert hasattr(base_command, 'config')
    assert hasattr(base_command, 'verbose')
    assert not base_command.verbose
    assert hasattr(base_command, 'ldap_server')
    assert isinstance(base_command.ldap_server, LDAPServer)
    assert not base_command.ldap_server.ldap_server
    base_command.bind_ldap()
    assert base_command.ldap_server.ldap_server
    base_command.unbind_ldap()
    assert not base_command.ldap_server.ldap_server
    assert hasattr(base_command, 'lp_client')
    assert isinstance(base_command.lp_client, LastPassClient)


def test_command_with_args():
    sys.argv = ['lpconnector', 'lastpassuser']
    args = ['--verbose', '--dry-run', '--url=test.com']
    command = commands.LastPassUsers('lastpassusers', args)
    assert hasattr(command, 'verbose')
    assert command.verbose
    assert hasattr(command, 'lp_client')
    lp_client = command.lp_client
    assert isinstance(lp_client, LastPassClient)
    assert lp_client.dry_run
    assert lp_client.url == 'test.com'
    sys.argv = []


def test_command_no_args(capsys):
    sys.argv = ['lpconnector', 'config']
    config_cmd = commands.Config('config', {})
    result = config_cmd.execute()
    assert result
    out, err = capsys.readouterr()
    assert err == ""
    assert out != ""
    sys.argv = []
