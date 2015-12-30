"""
Test end-to-end behavior.
"""
from mock import patch
from nagiosplugin import Runtime

from consulchecknagiosplugin.main import make_check
from consulchecknagiosplugin.format import DEFAULT_PATTERN
from consulchecknagiosplugin.resources import DEFAULT_HOST, DEFAULT_PORT
from consulchecknagiosplugin.tests.fixtures import mocked_get, NODE, OTHER_CHECK_ID


def test_main():
    """
    Ensure that calling check doesn't blow up.
    """
    check = make_check(
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        token=None,
        pattern=DEFAULT_PATTERN,
        node=NODE,
        check_id=OTHER_CHECK_ID,
    )
    with mocked_get(check.resources[0]):
        # reimplement `Check.main()` to get access to the Runtime (to disable exiting)
        runtime = Runtime()
        with patch.object(runtime, "sysexit"):
            runtime.execute(check, 1, 10)
