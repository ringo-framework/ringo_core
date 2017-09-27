#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Public API of the user model"""
from ringo_core.lib.db import get_db_session, session_scope
from ringo_core.model.user import User
from ringo_core.api.crud import (
    _create,
    _read,
    _update,
    _delete
)


def create(name, password):
    """Creates a new user with the given `name` and `password`.

    .. seealso:: Methods :func:`ringo_core.api.crud._create`

    :name: Name of the new user
    :password: Password (unencrypted) of the new user
    :returns: :class:`User` instance

    >>> import ringo_core.api.user
    >>> user = ringo_core.api.user.create(name="foo1", password="bar")
    >>> user.name
    'foo1'
    """
    with session_scope(get_db_session(), close=False) as db:
        user = _create(db, User, dict(name=name, password=password))
    return user


def read(item_id):
    """Read (load) a existing user from the database.

    .. seealso:: Methods :func:`ringo_core.api.crud._read`

    :item_id: ID of the user to load.
    :returns: :class:`User` instance


    >>> import ringo_core.api.user
    >>> # First create a new user.
    >>> newuser = ringo_core.api.user.create(name="foo2", password="bar")
    >>> # Now load the user
    >>> loaduser = ringo_core.api.user.read(item_id = newuser.id)
    >>> loaduser.name
    'foo2'
    """
    with session_scope(get_db_session(), close=False) as db:
        return _read(db, User, item_id)


def update(item_id, values):
    """Update a user with the given values in the database.

    .. seealso:: Methods :func:`ringo_core.api.crud._update`

    :item_id: ID of the user to update
    :values: Dictionary of values
    :returns: :class:`User` instance

    >>> import ringo_core.api.user
    >>> # First create a new user.
    >>> newuser = ringo_core.api.user.create(name="foo3", password="bar")
    >>> # Now load the user
    >>> values = {"name": "baz"}
    >>> updateduser = ringo_core.api.user.update(item_id = newuser.id, values=values)
    >>> updateduser.name
    'baz'
    """
    with session_scope(get_db_session(), close=False) as db:
        return _update(db, User, item_id, values)


def delete(item_id):
    """Deletes a user from the database.

    .. seealso:: Methods :func:`ringo_core.api.crud._delete`

    :item_id: ID of the user to update

    >>> import ringo_core.api.user
    >>> # First create a new user.
    >>> newuser = ringo_core.api.user.create(name="foo4", password="bar")
    >>> # Now delete the user
    >>> ringo_core.api.user.delete(item_id = newuser.id)
    >>> # Check that the user was actually deleted.
    >>> loaduser = ringo_core.api.user.read(item_id = newuser.id)
    Traceback (most recent call last):
        ...
    sqlalchemy.orm.exc.NoResultFound: No row was found for one()
    """
    with session_scope(get_db_session()) as db:
        return _delete(db, User, item_id)


def reset_password(item_id, password=None):
    """Will reset the password of the user.

    :item_id: ID of the user to update
    :password: Unencrypted password
    :returns: Unencrypted password

    .. seealso:: Methods :func:`ringo_core.model.user.reset_password`

    :item_id: ID of the user to update
    :password: Unencrypted password
    :returns: Unencrypted password

    >>> import ringo_core.api.user
    >>> # First create a new user.
    >>> newuser = ringo_core.api.user.create(name="foo5", password="bar")
    >>> oldpass = newuser.password
    >>> # Set custom password.
    >>> result = ringo_core.api.user.reset_password(item_id = newuser.id, password = "newpass")
    >>> result == "newpass"
    True
    >>> # Set random password.
    >>> result = ringo_core.api.user.reset_password(item_id = newuser.id)
    >>> result != "newpass"
    True
    """
    with session_scope(get_db_session()) as db:
        user = _read(db, User, item_id)
        new_password = user.reset_password(password)
    return new_password
