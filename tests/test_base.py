#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_base
----------------------------------

Tests for `ringo_core.model.base` module.
"""
import pytest
from ringo_core.model.base import Base


@pytest.fixture()
def newbase(db):
    base = Base()
    db.add(base)
    db.commit()
    return base


@pytest.fixture()
def loadedbase(db):
    base = Base()
    db.add(base)
    db.commit()
    base_id = base.id
    return db.query(Base).filter(Base.id == base_id).one()


def test_create_base():
    import uuid
    import datetime
    base = Base()
    assert base.id is None
    assert isinstance(base.uuid, uuid.UUID)
    assert isinstance(base.created, datetime.datetime)
    assert isinstance(base.updated, datetime.datetime)


def test_create_base_in_db(db, newbase):
    assert newbase.id == 1


def test_read_base_from_db(db, loadedbase):
    """Will check if all type of the item has correct types."""
    import uuid
    import datetime
    assert isinstance(loadedbase.id, int)
    assert isinstance(loadedbase.uuid, uuid.UUID)
    assert isinstance(loadedbase.created, datetime.datetime)
    assert isinstance(loadedbase.updated, datetime.datetime)


def test_update_base_from_db(db, loadedbase):
    """Will check if all values are actually updated, and the updated
    fields is updated."""
    loadedbase.id = 5
    old_updated = loadedbase.updated
    old_created = loadedbase.created
    db.commit()
    updateditem = db.query(Base).filter(Base.id == loadedbase.id).one()
    assert updateditem.id == 5

    # Now check that the updated attribute changed but not the created
    # item
    assert old_updated != updateditem.updated
    assert old_created == updateditem.created


def test_delete_base_from_db(db):
    """Will check if all values are actually updated, and the updated
    fields is updated."""
    all_items = db.query(Base).all()
    num = len(all_items)
    assert num >= 2

    last = all_items[-1]
    db.delete(last)
    db.commit()

    all_items = db.query(Base).all()
    assert num == len(all_items) + 1
