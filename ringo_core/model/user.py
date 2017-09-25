#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modul for Users"""
from ringo_core.lib.security import encrypt_password
from ringo_core.model.base import DBase, Base, BaseFactory


class UserFactory(BaseFactory):

    """Factory for user objects"""

    def create(self, name, password):
        """Will create a new :class:`User` object. The password will be
        encrypted.

        :name: Name of the new user. Used as for the username on
        authentification.
        :password: Unencrypted password of the new user.
        :returns: :class:`User` object.

        """
        encrypted_password = encrypt_password(password)
        return User(name, encrypted_password)


class User(Base, DBase):
    """User class"""

    def __init__(self, name, password):
        """TODO: to be defined1.

        :name: Name of the user used as username
        :password: Encrypted password of the user

        """
        super(User, self).__init__()

        self.name = name
        """Username of the user."""
        self.password = password
        """Encrypted password of the user."""

    @classmethod
    def get_factory(cls, db):
        return UserFactory(User, db)
