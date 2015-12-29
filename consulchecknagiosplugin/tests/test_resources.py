"""
Resource tests.
"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from consulchecknagiosplugin.resources import ConsulCheckHealth

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
