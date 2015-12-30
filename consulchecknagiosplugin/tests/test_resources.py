"""
Resource tests.
"""
from contextlib import contextmanager
from json import dumps

from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_,
)
from mock import patch

from consulchecknagiosplugin.resources import ConsulCheckHealth, ConsulCheck

CHECK_ID = "check-id"
OUTPUT = "output"


def test_parse_check_health():
    dct = {
        "CheckID": CHECK_ID,
        "Status": "passing",
        "Output": OUTPUT,
    }

    value = ConsulCheckHealth.from_dict(dct)
    assert_that(value.code, is_(equal_to(0)))
    assert_that(value.output, is_(equal_to(OUTPUT)))


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
            "CheckID": "serfHealth",
            "Status": "passing",
            "Output": "Agent alive and reachable",
        }, {
            "CheckID": "other",
            "Status": "critical",
            "Output": "Whatever",
        }])
        yield mocked_get
        mocked_get.assert_called_with(consul_check.url)


def test_get_node_health():
    check = ConsulCheck(
        host="localhost",
        port="8500",
        token=None,
        check_id="serfHealth",
    )
    with mocked_get(check):
        node_health = check.get_node_health()
        assert_that(node_health, has_length(2))


def test_get_check_health():
    check = ConsulCheck(
        host="localhost",
        port="8500",
        token=None,
        check_id="serfHealth",
    )
    with mocked_get(check):
        check_health = check.get_check_health()
        assert_that(check_health.code, is_(equal_to(0)))


def test_probe():
    check = ConsulCheck(
        host="localhost",
        port="8500",
        token=None,
        check_id="serfHealth",
    )
    with mocked_get(check):
        metrics = list(check.probe())
        assert_that(metrics, has_length(1))
        assert_that(metrics[0].value.code, is_(equal_to(0)))
