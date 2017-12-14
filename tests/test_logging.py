#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_security
----------------------------------

Tests for `tedega_share.lib.security` module.
"""
import pytest
import time
from tedega_share import log_proctime, monitor_system, monitor_connectivity, init_logger, get_logger


@log_proctime
def xxx():
    log = get_logger()
    log.debug("XXX")
    with pytest.raises(ValueError):
        log.debug("XXX", category="XXX")
    log.info("XXX")
    log.warning("XXX")
    log.error("XXX")


def test_logger():
    with pytest.raises(ValueError):
        get_logger()
    init_logger("xxx")
    monitor_connectivity([("www.google.de", "80"), ("www.hasahhshshshhshshs.de", "80")])
    monitor_system()
    xxx()
    time.sleep(10)


def test_buildtag():
    import os
    import socket
    from tedega_share.logger import build_tag
    hostname = socket.gethostname()
    tag = build_tag("xxx")
    assert tag == "%s.xxx" % hostname
    os.environ.setdefault("DOCKER_HOSTNAME", "foobar")
    tag = build_tag("xxx")
    assert tag == "foobar.xxx.%s" % hostname
