"""
Nagios Plugin resource(s).
"""
from collections import namedtuple
from json import loads
from logging import getLogger
from requests import get

from nagiosplugin import (
    CheckError,
    Metric,
    Resource,
)


CodeAndReason = namedtuple("CodeAndReason", ["code", "reason"])
PROXY = "proxy"


class ConsulNodeCheckStatus(Resource):
    """
    Returns node-specific check status and output information (from Consul).
    """
    def __init__(self,
                 host,
                 port,
                 token,
                 check_id):
        self.host = host
        self.port = port
        self.token = token
        self.check_id = check_id
        self.logger = getLogger('nagiosplugin')

    def get_node_health(self):
        """
        Query a Consul node for the health of all local checks.
        """
        url = "http://{}:{}/v1/health/node/{}?token=".format(
            self.host,
            self.port,
            self.host,
            self.token or ""
        )
        response = get(url)
        response.raise_for_status()

        # body will be a list of dictionaries with keys:
        #  - Node
        #  - CheckID
        #  - ServiceName
        #  - Notes
        #  - Status
        #  - ServiceID
        #  - Output

        return {
            check["CheckID"]: check
            for check in loads(response.text)
        }

    def get_check_health(self):
        """
        Query a Consul node for the health of a single check.

        Consul does not (yet?) have an API to query the outcome of a single check, so
        this function fetches all checks for a node and selects one.
        """
        node_health = self.get_node_health()
        try:
            return node_health[self.check_id]
        except KeyError:
            raise CheckError("No Consul data for check: '{}' on node '{}'".format(
                self.check_id,
                self.host,
            ))

    def probe(self):
        """
        Query consul for a specific check's health.

        Returns a metric with the checks status and output in its value.
        """
        check_health = self.get_check_health()
        value = CodeAndReason(
            code=check_health["Status"],
            reason=check_health["Output"],
        )
        yield Metric(self.check_id, value, context=PROXY)
