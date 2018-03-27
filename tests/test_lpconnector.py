import pytest
import docopt
from lpconnector.lpconnector import LPConnector


def test_lpconnector():
    with pytest.raises(docopt.DocoptExit):
        LPConnector()
