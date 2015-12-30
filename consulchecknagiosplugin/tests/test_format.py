"""
Resource tests.
"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from consulchecknagiosplugin.format import (
    DEFAULT_PATTERN,
    extract_line,
    summarize,
)


# Typical Consul output for a Serf Health Status check
SERF_LINE = "Agent alive and reachable"

# Consul URL checks may include large volumes of page content
HTTP_SUMMARY = "HTTP GET http://host:port/path: 200 OK"
HTTP_LINE = "{} Output: <HTML/>".format(HTTP_SUMMARY)


def test_summarize():
    assert_that(summarize("foo bar", 3), is_(equal_to("foo")))
    assert_that(summarize("foo bar", 3), is_(equal_to("foo")))


def test_extract_line():

    CASES = [
        # basic match
        (SERF_LINE, ".+", SERF_LINE),
        # match with group
        (SERF_LINE, "(.+)", SERF_LINE),
        # multi-line matching first line
        ("\n".join([SERF_LINE, SERF_LINE]), "(.+)", SERF_LINE),
        # multi-line matching second line
        ("\n".join(["", SERF_LINE]), "(.+)", SERF_LINE),
        # default pattern works for consul serf output
        (SERF_LINE, DEFAULT_PATTERN, SERF_LINE),
        # default pattern works for consul HTTP output
        (HTTP_LINE, DEFAULT_PATTERN, HTTP_SUMMARY),
    ]
    for output, pattern, line in CASES:
        yield assert_that, extract_line(output, pattern), is_(equal_to(line))
