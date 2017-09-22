#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_security
----------------------------------

Tests for `ringo_core.lib.security` module.
"""


def test_password_encryption():
    from ringo_core.lib.security import encrypt_password, verify_password
    password = "mysecurepassword"
    encrypt_password = encrypt_password(password)
    assert verify_password(password, encrypt_password)
    assert not verify_password(password+"xxx", encrypt_password)
