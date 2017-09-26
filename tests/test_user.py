#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model
----------------------------------

Tests for `ringo_core.model.user` module.
"""

import pytest


@pytest.fixture
def user_factory(db):
    from ringo_core.model.user import User
    return User.get_factory(db)


def test_create(user_factory):
    user = user_factory.create("foo@example.com", "mysecurepassword")
    assert user.name == "foo@example.com"
    assert user.password != "mysecurepassword"


def test_create_unique_name(db, user_factory):
    import sqlalchemy as sa
    user1 = user_factory.create("foo@example.com", "mysecurepassword")
    db.add(user1)
    user2 = user_factory.create("foo@example.com", "mysecurepassword")
    db.add(user2)
    with pytest.raises(sa.exc.IntegrityError):
        db.commit()
