from lpconnector.lpconnector import LPConnector


def test_lpconnector():

    connector = LPConnector()
    print connector.args
    assert hasattr(connector, 'args')
