#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_base
----------------------------------

Tests for `ringo_core.model.base` module.
"""
from datetime import datetime
import pytest
from sqlalchemy import event
from ringo_core.model.base import BaseItem
from ringo_core.lib.db import Base


class Dummy(BaseItem, Base):
    __tablename__ = "base"


@event.listens_for(Dummy, 'before_update')
def receive_before_update(mapper, connection, target):
    """Listen for the 'before_update' event. Make sure that the last
    updated field is updated as soon as the item has been modified.

    NOTE: The event is *not* triggered in case the uuid is changed. The
    reason is currently unknown. I expect this is a sideeffect of the
    defintion of a custom UUID type.
    """
    if hasattr(target, "updated"):
        target.updated = datetime.utcnow()


@pytest.fixture()
def newbase(db):
    base = Dummy()
    db.add(base)
    db.commit()
    return base


@pytest.fixture()
def loadedbase(db):
    base = Dummy()
    db.add(base)
    db.commit()
    base_id = base.id
    return db.query(Dummy).filter(Dummy.id == base_id).one()


def test_create_base():
    import uuid
    import datetime
    base = Dummy()
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
    import uuid
    loadedbase.uuid = uuid.uuid4()
    old_updated = loadedbase.updated
    old_created = loadedbase.created
    db.commit()
    updateditem = db.query(Dummy).filter(Dummy.id == loadedbase.id).one()

    # Now check that the updated attribute changed but not the created
    # item
    assert old_updated != updateditem.updated
    assert old_created == updateditem.created


def test_delete_base_from_db(db):
    """Will check if all values are actually updated, and the updated
    fields is updated."""
    all_items = db.query(Dummy).all()
    num = len(all_items)
    assert num >= 2

    last = all_items[-1]
    db.delete(last)
    db.commit()

    all_items = db.query(Dummy).all()
    assert num == len(all_items) + 1
