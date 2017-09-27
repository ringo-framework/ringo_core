#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

DEFAUL_DB_URI = "sqlite:///:memory:"
DB_URI = os.environ.get("RINGO_CORE_DB_URI", DEFAUL_DB_URI)
ENGINE = create_engine(DB_URI, echo=False)


def init_db(engine=None):
    if engine is None:
        engine = ENGINE
    Base.metadata.create_all(engine)


def get_db_engine(uri=None, echo=False):
    """

    :uri: Connection string to the database.
    :echo: Flag to enabled debug output of sqlalchemy.
    :returns: database engine

    """
    global ENGINE
    if uri is None:
        return ENGINE
    else:
        return create_engine(uri, echo=echo)


def get_db_session(uri=None):
    """Return a db session to the given database defined by the URI

    :uri: TODO
    :returns: TODO

    """
    engine = get_db_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()


@contextmanager
def session_scope(session, close=True):
    """Provide a transactional scope around a series of operations. The
    transaction takes care that the session is commited or rollback in
    case of errors and finally closed. Optionally you can choose to not
    close the session to leave items loaded from the session detached
    and further accessible. Otherwise you will get a DetachedInstance
    error when trying to access any value of the item.

    :session: Session instance
    :close: Flag to disable closing the session. Default is to close the
            session.
    """
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        if close:
            session.close()
