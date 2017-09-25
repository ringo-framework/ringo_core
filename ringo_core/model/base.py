#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
import sqlalchemy as sa
from ringo_core.model.datatypes import UUID
from ringo_core.lib.db import DBase


def create_model(engine):
    DBase.metadata.create_all(engine)


class BaseFactory(object):

    """Factory for base objects"""

    def __init__(self, clazz, db):
        self.clazz = clazz
        self.db = db

    def create(self):
        """Will create a new :class:`Base` object.
        :returns: :class:`Base` object.

        """
        return self.clazz()

    def load(self, item_id):
        """Will create a new :class:`Base` object.
        :returns: :class:`Base` object.

        """
        return self.db.query(self.clazz).filter(self.clazz.id == item_id).one()


class BaseItem(object):
    """Base for all models in Ringo"""

    id = sa.Column("id", sa.Integer, primary_key=True)
    """Local unique identifier within the database. Used to load datasets
    from the database."""

    created = sa.Column("uuid", UUID)
    """Globally unique indentifier."""

    created = sa.Column("created", sa.DateTime)
    """Datetime when the dataset was created."""

    updated = sa.Column("updated", sa.DateTime)
    """Datetime when the dataset was last modfied."""

    def __init__(self):
        self.id = None
        self.uuid = uuid.uuid4()
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()

    @classmethod
    def get_factory(cls, db):
        """Return an instance of a factory for this class."""
        return BaseFactory()


@event.listens_for(Base, 'before_update')
def receive_before_update(mapper, connection, target):
    """Listen for the 'before_update' event. Make sure that the last
    updated field is updated as soon as the item has been modified.

    NOTE: The event is *not* triggered in case the uuid is changed. The
    reason is currently unknown. I expect this is a sideeffect of the
    defintion of a custom UUID type.
    """
    if hasattr(target, "updated"):
        target.updated = datetime.utcnow()
