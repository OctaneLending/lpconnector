import pytest
import docopt
from lpconnector.lpconnector import LPConnector


def test_lpconnector_no_cmd():
    with pytest.raises(docopt.DocoptExit):
        LPConnector()


def test_lpconnector_valid_cmd():
    args = ['config']
    connector = LPConnector(args)
    assert hasattr(connector, 'config') and hasattr(connector, 'args') and connector.args.get('<command>') == 'config'


def test_lpconnector_invalid_cmd():
    args = ['notacmd']
    with pytest.raises(docopt.DocoptExit):
        LPConnector(args)