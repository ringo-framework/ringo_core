#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tediga provides logging capabilities to applications to ensure that the
data is logged in a consistent manner, which is a prerequisite for later
evaluation.

Tedega uses Fluentd Logs for centralized logging. This collects all logs
into a uniform form, and stores them in different backends as needed.
From there, the logs can then be analyzed using tools such as
Elasticsearch or Hadop.

The following categories are logged:

* **Requests**. All requests to the application are logged. The
  Includes the url, method (GET, POST, PUT ...) and possible parameters. They
  are marked in the category *REQUEST*.

* **Processing time**. Every request to a service will have the
  response time logged in milliseconds that a service needs to answer a
  request. The time adds up to the necessary steps for the answering be
  carried out. So also possible queries to others services. The category
  for the processing time is *PROCTIME*

* **Status response**. Each request logs the HTTP status of it
  answer. The category for the status is *RETURNCODE*

* **Reachability**. Periodically, each service is will check its
  connecivity to other hosts and services. Accessibility messages have the
  category *PING*.

* **Utilization RAM, CPU, memory**. We pick up at regular intervals
  information about the load of RAM, load and
  storage space in order to detect bottlenecks early. The
  corresponding category is *SYSTEM*.

* **More information**. In addition to the information described above,
  of course also any other information can be logged as needed. These
  should then be categorized with *CUSTOM*.

So that the messages are systematically evaluated in a central location
all messages must be in a predefined format. Each
Log message has a tag which Fluentd uses to route log messages
can be used::

        <HOST>. <SERVICE> [. <CONTAINER>]

The actual log message is saved in JSON format::

        {
            "type": "INFO",
            "category": null,
            "correlation_id": null,
            "extra_key_depending_on_category": "value"
        }

The following table provides information about the most important tags
in log messages.

============== ================
Section        Description
============== ================
HOST           Name of the computer.
CONTAINER      Name Containers.
SERVICE        Name of the service
CATEGORY       Type of log message.
CORRELATION_ID When a request first encounters a service, it generates a unique UUID, which is used in all subsequent queries to track related messages across different services. This information is optional because not all messages are generated in services or require such a UUID.
LEVEL          Indicates whether the message is an ERROR, a WARNING, an INFO, or a DEBUG output. The default for a message is INFO.
============== ================


"""

import threading
import collections
import socket
import time
import os
import logging
import voorhees
import psutil
from fluent import handler

custom_format = {
    'host': '%(hostname)s',
    # 'where': '%(module)s.%(funcName)s',
    # 'type': '%(levelname)s',
    # 'stack_trace': '%(exc_text)s'
}

CATEGORIES = ["PING", "SYSTEM", "PROCTIME",
              "RETURNCODE", "REQUEST", "AUTH", "CUSTOM"]

log = None


def log_proctime(func):
    """Decorator to log the processing time of the decorated method."""
    def wrap(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        log.info({"time": time.time() - started_at, "func": "%s.%s" % (func.__module__, func.__name__)}, "PROCTIME")
        return result
    return wrap


def monitor_system(interval=300, duration=10):
    """Continually logging of CPU, RAM and DISK usage in the
    given intervall in seconds. The CPU will be the averange for the
    given duration.

    :interval: Check will be executed every X seconds
    :duration: CPU is the averange of the given duration
    """
    def worker():
        while 1:
            _log_system(duration)
            time.sleep(interval)
    t = threading.Thread(name="monitor_system", target=worker, daemon=True)
    t.start()


def _log_system(interval):
    cpu = psutil.cpu_percent(interval=interval, percpu=False)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    log.info({"cpu": cpu, "memory": memory, "disk": disk}, "SYSTEM")


def monitor_connectivity(hosts, interval=60):
    """Continually check and log the connection to the list of given
    hosts in the given intervall in seconds.

    :hosts: List of tuples (hostname, port)
    :interval: Check will be executed every X seconds
    """
    def worker(hosts):
        while 1:
            _log_connectivity(hosts)
            time.sleep(interval)
    t = threading.Thread(name="monitor_connectivity", target=worker, args=(hosts,), daemon=True)
    t.start()


def _log_connectivity(hosts):
    result = collections.OrderedDict()
    for host, port in hosts:
        try:
            socket.create_connection((host, port))
            result[host] = True
        except OSError:
            result[host] = False
    log.info(result, "PING")


class Logger(object):
    """Wrapper around the Python logger to ensure a specific log
    format."""
    def __init__(self, logger, service):
        self._logger = logger
        self._service = service

    def _build_message(self, message, category, correlation_id):
        if category is not None and category not in CATEGORIES:
            raise ValueError("{} logging category unknown.".format(category))
        msg = collections.OrderedDict()
        msg["service"] = self._service
        msg["category"] = category
        msg["correlation_id"] = correlation_id

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


def init_logger(service, host="localhost", port=24224):
    """Will initialise a global :class:`Logger` instance to log to fluentd.

    :tag: String used as tag for fluentd log routing.
    :host: Host where the fluentd is listening
    :port: Port where the fluentd is listening

    """

    tag = build_tag(service)
    logging.basicConfig(level=logging.INFO)
    l = logging.getLogger(tag)
    h = handler.FluentHandler(tag, host=host, port=port)
    formatter = handler.FluentRecordFormatter(custom_format)
    h.setFormatter(formatter)
    l.addHandler(h)

    global log
    log = Logger(l, service)


def get_logger():
    """Will return the global :class:`Logger` instance. Will raise an
    exception if the Logger is not initialised.

    :returns: Logger instance
    """
    global log
    if log:
        return log
    raise ValueError("Logger is not initialised!")
