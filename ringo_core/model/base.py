#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base

from ringo_core.model.datatypes import UUID

DBase = declarative_base()


def create_model(engine):
    DBase.metadata.create_all(engine)


class Base(DBase):
    """Base for all models in Ringo"""
    __tablename__ = "base"

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
