#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_crud
----------------------------------

Tests for `ringo_core.api.crud` module.
"""
import pytest
from ringo_storage import get_storage
from ringo_core.model.user import User


def test_searech_fail_because_not_base(storage):
    from ringo_core.api.crud import _search
    with pytest.raises(TypeError):
        _search(storage, object)


def test_create_fail_because_not_base(storage):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        _create(storage, object, {})


def test_read_fail_because_not_base(storage):
    from ringo_core.api.crud import _read
    with pytest.raises(TypeError):
        _read(storage, object, 12)


def test_read_fail_because_not_integer(storage):
    from ringo_core.api.crud import _read
    with pytest.raises(TypeError):
        _read(storage, User, "12")


def test_update_fail_because_not_base(storage):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(storage, object, 12, {})


def test_update_fail_because_not_integer(storage):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(storage, User, "12", {})


def test_create_fail_because_not_dict(storage):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        _create(storage, User, "Value")


def test_update_fail_because_not_dict(storage):
    from ringo_core.api.crud import _update
    with pytest.raises(TypeError):
        _update(storage, User, 12, "Value")


def test_create_fail_because_wrong_paramaters(storage):
    from ringo_core.api.crud import _create
    with pytest.raises(TypeError):
        # User create does not expect "foo"
        _create(storage, User, {"foo": "bar"})


@pytest.mark.parametrize("clazz, values, expected", [
    (User, {"name": "Foo", "password": "test"}, {"name": "Foo"}),
])
def test_create(clazz, values, expected):
    from ringo_core.api.crud import _create

    with get_storage() as storage:
        instance = _create(storage, clazz, values)
        assert instance.id is not None
        assert isinstance(instance.id, int)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, item_id, expected", [
    (User, 1, {"name": "Foo"}),
])
def test_read(clazz, item_id, expected):
    from ringo_core.api.crud import _read

    with get_storage() as storage:
        instance = _read(storage, clazz, item_id)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, item_id, values, expected", [
    (User, 1, {"name": "Foo2"}, {"name": "Foo2"}),
])
def test_update(clazz, item_id, values, expected):
    from ringo_core.api.crud import _update

    with get_storage() as storage:
        instance = _update(storage, clazz, item_id, values)
        for key in expected:
            assert getattr(instance, key) == expected[key]


@pytest.mark.parametrize("clazz, values", [
    (User, {"name": "Foo", "password": "test"}),
])
def test_delete(storage, clazz, values):
    from ringo_core.api.crud import _create, _delete

    with get_storage() as storage:
        instance = _create(storage, clazz, values)
        item_id = instance.id

    with get_storage() as storage:
        num_items = len(storage.session.query(clazz).all())
        _delete(storage, clazz, item_id)

    with get_storage() as storage:
        num_items_after_delete = len(storage.session.query(clazz).all())

    assert num_items_after_delete == (num_items - 1)
