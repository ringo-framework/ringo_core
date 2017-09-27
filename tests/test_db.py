#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_db
----------------------------------

Tests for `ringo_core.lib.db` module.
"""
import pytest


def test_get_engine():
    from ringo_core.lib.db import get_db_engine
    engine = get_db_engine('sqlite:///:memory:')
    assert engine is not None


def test_get_dbsession():
    from ringo_core.lib.db import get_db_session
    session = get_db_session()
    assert session is not None


def test_get_scopedsession():
    from ringo_core.lib.db import get_db_session
    from ringo_core.lib.db import session_scope
    session = get_db_session()
    with session_scope(session) as session:
        assert session is not None


def test_get_scopedsession_rollback():
    from ringo_core.lib.db import get_db_session
    from ringo_core.lib.db import session_scope
    session = get_db_session()
    with pytest.raises(Exception):
        with session_scope(session) as session:
            session.execute("Foo")
    assert session is not None


def test_get_scopedsession_detach_exception(db):
    from sqlalchemy.orm.exc import DetachedInstanceError
    from ringo_core.lib.db import session_scope
    from ringo_core.model.user import User
    with pytest.raises(DetachedInstanceError):
        with session_scope(db) as session:
            factory = User.get_factory(db)
            new = factory.create("Foo", "Bar")
            session.add(new)
            session.flush()

        # No outside the scope. Session has been already closed and the
        # instance is detached from the session. I expect
        # a exection when accessing any attribute of the instance.
        assert new.id is not None
