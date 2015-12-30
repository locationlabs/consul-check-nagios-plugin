# consul-check-nagios-plugin

Consul Check Nagios Plugin

Translates a Consul check into Nagios output.

[![Build Status](https://travis-ci.org/locationlabs/consul-check-nagios-plugin.png)](https://travis-ci.org/locationlabs/consul-check-nagios-plugin)

## Installation

Use pip:

    pip install consulchecknagiosplugin


## Usage

The basic usage is:

    check-consul <node-name> <check-name>

By default, the check assumes it will connext to a local Consul agent; this behavior can be overridden
using CLI arguments.
