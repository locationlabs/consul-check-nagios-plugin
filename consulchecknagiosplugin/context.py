"""
Nagios Plugin context(s).
"""
from nagiosplugin import (
    Context,
    Critical,
    Ok,
    Unknown,
    Warn,
)


STATES = {
    state.code: state for state in [Critical, Ok, Unknown, Warn]
}


class PassThroughContext(Context):
    """
    Context that reports another system's status verbatim.
    """

    NAME = "PASS"

    def __init__(self):
        super(PassThroughContext, self).__init__(PassThroughContext.NAME)

    def evaluate(self, metric, resource):
        """
        Evaluate the metric by passing its code and reason through.
        """
        state = STATES.get(metric.value.code, Unknown)
        return self.result_cls(state, metric.value.reason, metric)
