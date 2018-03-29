import sys
import pytest
import docopt
from lpconnector.lpconnector import LPConnector


def test_lpconnector_no_cmd():
    with pytest.raises(docopt.DocoptExit):
        LPConnector()


def test_lpconnector_valid_cmd():
    sys.argv = ['lpconnector', 'config']
    connector = LPConnector()
    assert hasattr(connector, 'config') and hasattr(connector, 'args') and connector.args.get('<command>') == 'config'
    sys.argv = []
