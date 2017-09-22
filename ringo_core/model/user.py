#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modul for Users"""
from ringo_core.lib.security import encrypt_password
from ringo_core.model.base import Base


class UserFactory(object):

    """Factory for user objects"""

    def __init__(self):
        """TODO: to be defined1. """

    def create(self, email, password):
        """Will create a new :class:`User` object. The password will be
        encrypted.

        :email: E-Mail of the new user. Used as for the username.
        :password: Unencrypted password of the new user.
        :returns: :class:`User` object.

        """
        encrypted_password = encrypt_password(password)
        return User(email, encrypted_password)


class User(Base):

    """User class"""

    def __init__(self, email, password):
        """TODO: to be defined1.

        :email: E-Mail of the user used as username
        :password: Encrypted password of the user

        """
        super(User, self).__init__()

        self.name = email
        """Username of the user."""
        self.password = password
        """Encrypted password of the user."""
