#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_crud
----------------------------------

Tests for `ringo_core.api.crud` module.
"""
import pytest
from ringo_core.model.user import User


def test_create_fail_because_not_base(db):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        _create(db, object, {})


def test_read_fail_because_not_base(db):
    from ringo_core.api.crud import _read
    with pytest.raises(TypeError):
        _read(db, object, 12)


def test_read_fail_because_not_integer(db):
    from ringo_core.api.crud import _read
    with pytest.raises(TypeError):
        _read(db, User, "12")


def test_update_fail_because_not_base(db):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(db, object, 12, {})


def test_update_fail_because_not_integer(db):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(db, User, "12", {})


def test_create_fail_because_not_dict(db):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        _create(db, User, "Value")


def test_update_fail_because_not_dict(db):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(db, User, 12, "Value")


def test_create_fail_because_wrong_paramaters(db):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        # User create does not expect "foo"
        _create(db, User, {"foo": "bar"})


@pytest.mark.parametrize("clazz, values, expected", [
    (User, {"name": "Foo", "password": "test"}, {"name": "Foo"}),
])
def test_create(db, clazz, values, expected):
    from ringo_core.api.crud import _create
    from ringo_core.lib.db import session_scope

    with session_scope(db) as session:
        instance = _create(db, clazz, values)
        assert instance.id is not None
        assert isinstance(instance.id, int)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, item_id, expected", [
    (User, 1, {"name": "Foo"}),
])
def test_read(db, clazz, item_id, expected):
    from ringo_core.api.crud import _read
    from ringo_core.lib.db import session_scope

    with session_scope(db) as session:
        instance = _read(session, clazz, item_id)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, item_id, values, expected", [
    (User, 1, {"name": "Foo2"}, {"name": "Foo2"}),
])
def test_update(db, clazz, item_id, values, expected):
    from ringo_core.api.crud import _update
    from ringo_core.lib.db import session_scope

    with session_scope(db) as session:
        instance = _update(session, clazz, item_id, values)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, values", [
    (User, {"name": "Foo", "password": "test"}),
])
def test_delete(db, clazz, values):
    from ringo_core.api.crud import _create, _delete
    from ringo_core.lib.db import session_scope

    with session_scope(db) as session:
        instance = _create(db, clazz, values)
        item_id = instance.id

    with session_scope(db) as session:
        num_items = len(db.query(clazz).all())
        _delete(session, clazz, item_id)

    with session_scope(db) as session:
        num_items_after_delete = len(db.query(clazz).all())

    assert num_items_after_delete == (num_items - 1)
