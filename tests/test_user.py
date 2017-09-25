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
