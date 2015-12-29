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


class ProxyContext(Context):
    """
    Context that reports another system's status verbatim.
    """
    def __init__(self, name):
        super(ProxyContext, self).__init__(
            name=name,
        )

    def evaluate(self, metric, resource):
        state = STATES.get(metric.value.code, Unknown)
        return self.result_cls(state, metric.value.reason, metric)
