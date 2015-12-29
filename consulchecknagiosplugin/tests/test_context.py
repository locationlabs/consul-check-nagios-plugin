"""
Test Context behavior.
"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)
from mock import MagicMock

from consulchecknagiosplugin.context import PassThroughContext
from nagiosplugin import Critical, Ok, Warn, Unknown


REASON = "reason"


def test_evaluate():
    """
    Validate that PassThroughContext handles error codes properly.
    """
    def do_evaluate(context, metric, resource, state):
        result = context.evaluate(metric, resource)
        assert_that(result.state, is_(equal_to(state)))
        assert_that(result.hint, is_(equal_to(REASON)))

    CASES = {
        0: Ok,
        1: Warn,
        2: Critical,
        3: Unknown,
        None: Unknown,
    }

    for code, state in CASES.items():
        context = PassThroughContext()
        metric, resource = MagicMock(), MagicMock()
        metric.value.code = code
        metric.value.reason = REASON
        yield do_evaluate, context, metric, resource, state
