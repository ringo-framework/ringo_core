#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_db_engine(uri='sqlite:///:memory:'):
    """

    :uri: Connection string to the database.
    :returns: database engine

    """
    engine = create_engine('sqlite:///:memory:', echo=True)
    return engine


def get_db_session(uri='sqlite:///:memory:'):
    """Return a db session to the given database defined by the URI

    :uri: TODO
    :returns: TODO

    """
    engine = get_db_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()
