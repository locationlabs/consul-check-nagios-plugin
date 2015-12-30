"""
Test fixtures.
"""
from contextlib import contextmanager
from json import dumps

from mock import patch


SERF_CHECK_ID = "serfHealth"
OTHER_CHECK_ID = "other"


@contextmanager
def mocked_get(consul_check):
    """
    Test fixture for mocking Consul query.
    """
    with patch("consulchecknagiosplugin.resources.get") as mocked_get:
        # inject test data
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.reason = "OK"
        mocked_get.return_value.text = dumps([{
            "CheckID": SERF_CHECK_ID,
            "Status": "passing",
            "Output": "Agent alive and reachable",
        }, {
            "CheckID": OTHER_CHECK_ID,
            "Status": "critical",
            "Output": "Whatever | it is",
        }])
        yield mocked_get
        mocked_get.assert_called_with(consul_check.url)
