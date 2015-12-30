"""
Test Context behavior.
"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)
from nagiosplugin import Critical, Metric, Ok, Warn, Unknown

from consulchecknagiosplugin.context import PassThroughContext
from consulchecknagiosplugin.resources import ConsulCheckHealth, ConsulCheck


CHECK_ID = "serfHealth"
LINE = "line"


def test_evaluate():
    """
    Validate that PassThroughContext handles error codes properly.
    """
    def do_evaluate(context, metric, resource, state):
        result = context.evaluate(metric, resource)
        assert_that(result.state, is_(equal_to(state)))
        assert_that(result.hint, is_(equal_to(LINE)))

    CASES = {
        0: Ok,
        1: Warn,
        2: Critical,
        3: Unknown,
        None: Unknown,
    }

    for code, state in CASES.items():
        context = PassThroughContext()
        metric = Metric(CHECK_ID, ConsulCheckHealth(code, LINE), context=PassThroughContext.NAME)
        resource = ConsulCheck(CHECK_ID)
        yield do_evaluate, context, metric, resource, state
