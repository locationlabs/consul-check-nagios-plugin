"""
Resource tests.
"""
from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_,
)

from consulchecknagiosplugin.resources import ConsulCheckHealth, ConsulCheck
from consulchecknagiosplugin.tests.fixtures import mocked_get, NODE, SERF_CHECK_ID


OUTPUT = "output"


def test_parse_check_health():
    dct = {
        "CheckID": SERF_CHECK_ID,
        "Status": "passing",
        "Output": OUTPUT,
    }

    value = ConsulCheckHealth.from_dict(dct)
    assert_that(value.code, is_(equal_to(0)))
    assert_that(value.output, is_(equal_to(OUTPUT)))


def test_get_node_health():
    check = ConsulCheck(
        node=NODE,
        check_id=SERF_CHECK_ID,
    )
    with mocked_get(check):
        node_health = check.get_node_health()
        assert_that(node_health, has_length(2))


def test_get_check_health():
    check = ConsulCheck(
        node=NODE,
        check_id=SERF_CHECK_ID,
    )
    with mocked_get(check):
        check_health = check.get_check_health()
        assert_that(check_health.code, is_(equal_to(0)))


def test_probe():
    check = ConsulCheck(
        node=NODE,
        check_id=SERF_CHECK_ID,
    )
    with mocked_get(check):
        metrics = list(check.probe())
        assert_that(metrics, has_length(1))
        assert_that(metrics[0].value.code, is_(equal_to(0)))
