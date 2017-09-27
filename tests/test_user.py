#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model
----------------------------------

Tests for `ringo_core.model.user` module.
"""

import pytest


def test_not_found():
    import sqlalchemy as sa
    import ringo_core.api.user
    with pytest.raises(sa.orm.exc.NoResultFound):
        ringo_core.api.user.read(9999)


def test_create(randomstring):
    import ringo_core.api.user
    name = randomstring(8)
    user = ringo_core.api.user.create(name=name, password="password")
    assert user.name == name


def test_create_unique_name(randomstring):
    import sqlalchemy as sa
    import ringo_core.api.user
    name = randomstring(8)
    user = ringo_core.api.user.create(name=name, password="password")
    assert user.name == name
    with pytest.raises(sa.exc.IntegrityError):
        user = ringo_core.api.user.create(name=name, password="password")


def test_read(randomstring):
    import ringo_core.api.user
    name = randomstring(8)
    user = ringo_core.api.user.create(name=name, password="password")
    loaded = ringo_core.api.user.read(user.id)
    assert loaded.name == name


def test_update(randomstring):
    import ringo_core.api.user
    name = randomstring(8)
    user = ringo_core.api.user.create(name=name, password="password")
    values = {"name": "updated"}
    updated = ringo_core.api.user.update(user.id, values)
    assert updated.name == "updated"
    assert updated.updated != user.updated


def test_delete(randomstring):
    import sqlalchemy as sa
    import ringo_core.api.user
    name = randomstring(8)
    user = ringo_core.api.user.create(name=name, password="password")
    ringo_core.api.user.delete(user.id)
    with pytest.raises(sa.orm.exc.NoResultFound):
        user = ringo_core.api.user.read(9999)
