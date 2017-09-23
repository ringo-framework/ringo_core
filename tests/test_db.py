#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_db
----------------------------------

Tests for `ringo_core.lib.db` module.
"""


def test_get_engine():
    from ringo_core.lib.db import get_db_engine
    engine = get_db_engine()
    assert engine is not None


def test_get_dbsession():
    from ringo_core.lib.db import get_db_session
    session = get_db_session()
    assert session is not None
