#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from ringo_core.model.datatypes import UUID

DBase = declarative_base()

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
