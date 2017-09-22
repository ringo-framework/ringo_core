#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_base
----------------------------------

Tests for `ringo_core.model.base` module.
"""


def test_base():
    from ringo_core.model.base import Base

    base = Base()
    assert base.id is None
    assert base.uuid is None
    assert base.created is None
    assert base.updated is None
