#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_base
----------------------------------

Tests for `ringo_core.model.base` module.
"""


def test_base():
    import uuid
    import datetime
    from ringo_core.model.base import Base

    base = Base()
    assert base.id is None
    assert isinstance(base.uuid, uuid.UUID)
    assert isinstance(base.created, datetime.datetime)
    assert isinstance(base.updated, datetime.datetime)
