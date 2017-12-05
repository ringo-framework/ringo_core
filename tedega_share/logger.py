#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import logging
import voorhees
from fluent import handler

custom_format = {
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s'
}

CATEGORIES = ["PING", "CPU", "RAM", "DISK", "PROCTIME",
              "RETURNCODE", "REQUEST", "AUTH", "CUSTOM"]


class Logger(object):
    """Wrapper around the Python logger to ensure a specific log
    format."""

    def __init__(self, logger, service):
        self._logger = logger
        self._service = service

    def _build_message(self, message, category, correlation_id):
        if category is not None and category not in CATEGORIES:
            raise ValueError("{} logging category unknown.".format(category))
        msg = {}
        msg["category"] = category
        msg["correlation_id"] = correlation_id
        msg["service"] = self._service

        if isinstance(message, dict):
            msg.update(message)
        else:
            msg["message"] = message
        return voorhees.to_json(msg)

    def debug(self, message, category=None, correlation_id=None):
        """Write a debug message."""
        message = self._build_message(message, category, correlation_id)
        self._logger.debug(message)

    def info(self, message, category=None, correlation_id=None):
        """Write a info message."""
        message = self._build_message(message, category, correlation_id)
        self._logger.info(message)

    def error(self, message, category=None, correlation_id=None):
        """Write a error message."""
        message = self._build_message(message, category, correlation_id)
        self._logger.error(message)

    def warning(self, message, category=None, correlation_id=None):
        """Write a warning message."""
        message = self._build_message(message, category, correlation_id)
        self._logger.warning(message)


def build_tag(service):
    """Will build a tag used to tag fluentd log messages. The tag has
    the format <hostname>.<service>[.<container>]'

    The `hostname` is determined from the DOCKER_HOSTNAME
    environment variable. If the variable is not set (e.g the service is
    not running in a docker container) the hostname is set to the
    systems hostname.

    The `container` is determined by the systems hostname which is the
    docker container ID in case the service runs in a docker container.
    Otherwise the container is equal to the `hostname` and will be
    omitted in the tag.

    :service: Name of the microservice
    :returns: Logging tag

    """
    tag = []
    hostname = os.environ.get("DOCKER_HOSTNAME", socket.gethostname())
    tag.append(hostname)
    tag.append(service)
    container = socket.gethostname()
    if hostname != container:
        tag.append(container)
    return ".".join(tag)


def get_logger(service, host="localhost", port=24224):
    """Will return a Logger instance to log to fluentd.

    :tag: String used as tag for fluentd log routing.
    :host: Host where the fluentd is listening
    :port: Port where the fluentd is listening
    :returns: Logger instance

    """
    tag = build_tag(service)
    logging.basicConfig(level=logging.INFO)
    l = logging.getLogger(tag)
    h = handler.FluentHandler(tag, host=host, port=port)
    formatter = handler.FluentRecordFormatter(custom_format)
    h.setFormatter(formatter)
    l.addHandler(h)
    return Logger(l, service)


if __name__ == "__main__":
    log = get_logger("testservice")
    log.info("Test")
    log.info({"Foo": "Bar"})
