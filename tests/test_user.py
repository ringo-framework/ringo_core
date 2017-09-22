#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_model
----------------------------------

Tests for `ringo_core.model.user` module.
"""

import pytest


@pytest.fixture
def user_factory():
    from ringo_core.model.user import UserFactory
    return UserFactory()


def test_create(user_factory):
    user = user_factory.create("foo@example.com", "mysecurepassword")
    assert user.name == "foo@example.com"
    assert user.password != "mysecurepassword"
