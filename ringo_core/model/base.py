#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime


class Base(object):
    """Base for all models in Ringo"""

    def __init__(self):
        self.id = None
        """Unique identifier within the database. Used to load datasets
        from the database."""
        self.uuid = uuid.uuid4()
        """Globally unique indentifier."""
        self.created = datetime.utcnow()
        """Datetime when the dataset was created."""
        self.updated = datetime.utcnow()
        """Datetime when the dataset was last modfied."""
