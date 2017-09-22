#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Base(object):
    """Base for all models in Ringo"""

    def __init__(self):
        self.id = None
        """Unique identifier within the database. Used to load datasets
        from the database."""
        self.uuid = None
        """Globally unique indentifier."""
        self.created = None
        """Datetime when the dataset was created."""
        self.updated = None
        """Datetime when the dataset was last modfied."""
