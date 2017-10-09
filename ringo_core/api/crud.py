#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Internal API for CRUD actions. These methods provide elementary
functionality to create, read, update and delete elements from database.
These methods are **not** menat to be used directly. The are used by
public API.

The methods are kept very simple and does nothing than actually reading
and writing to the database.

.. warning::
    This API is an internal API and is **not** meant to be used directly!

"""
import sqlalchemy as sa
from ringo_service.api import NotFound, ClientError
from ringo_core.model.base import BaseItem


def _search(db, clazz, limit=20, offset=0, search=""):
    """Will return all instances of `clazz`.

    :db: Session to the database.
    :clazz: Class of which the instances should be loaded.
    :limit: Limit number of result to N entries
    :offset: Return entries with an offset of N
    :returns: List of instances of clazz
    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))

    query = db.query(clazz)

    # Handle search filters.
    if search != "":
        try:
            for _filter in search.split("|"):
                key, value = _filter.split("::")
                query = query.filter(getattr(clazz, key) == value)
        except ValueError:
            raise ClientError("Can not parse search filter")
        except AttributeError:
            # Key in search filter is not existing
            raise ClientError("One of the fields in search filter are invalid")

    return query.slice(offset, limit).all()


def _create(db, clazz, values):
    """Will return a new instance of `clazz`. The new instance will be
    added to the given `db` session and is initiated with the given
    `values`

    .. seealso::

        Create method of the specific factory of `clazz`

    `clazz` must be a subclass of :class:`BaseItem`. If not a TypeError
    will be raised.
    `values` must be of type dict. If not a TypeError will be raised.

    :db: Session to the database.
    :clazz: Class of which an instance should be created.
    :values: Dictionary of values used for initialisation.
    :returns: Instance of clazz
    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))
    if not isinstance(values, dict):
        raise TypeError("Create must be called with a values of type {}".format(dict))
    factory = clazz.get_factory(db)
    try:
        instance = factory.create(**values)
    except TypeError as e:
        raise TypeError("{}.{}".format(factory.__class__.__name__, e))

    # Add new instance to the session and flush to make the id of
    # the new instance appear.
    db.add(instance)
    db.flush()
    return instance


def _read(db, clazz, item_id):
    """Will return a instance of `clazz`. The instance is read from the
    given `db` session.

    .. seealso::

        `load` method of the specific factory of `clazz`

    `clazz` must be a subclass of :class:`BaseItem`. If not a TypeError
    will be raised.
    `item_id` must be of type integer. If not a TypeError will be raised.

    :db: Session to the database.
    :clazz: Class of which an instance should be loaded.
    :item_id: ID of the item which should be loaded.
    :returns: Instance of clazz

    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))
    if not isinstance(item_id, int):
        raise TypeError("item_id must be called with a value of type {}".format(int))
    factory = clazz.get_factory(db)
    try:
        instance = factory.load(item_id)
    except sa.orm.exc.NoResultFound:
        raise NotFound()
    return instance


def _update(db, clazz, item_id, values):
    """Will update a instance of `clazz`. The instance is read from the
    given `db` session and then updated with the given values. Values
    for attributes which are not part of `clazz` are silently ignored.

    .. seealso::

        `load` method of the specific factory of `clazz`
        values Me
        `set_values` method of the specific `clazz`

    `clazz` must be a subclass of :class:`BaseItem`. If not a TypeError
    will be raised.
    `item_id` must be of type integer. If not a TypeError will be raised.
    `values` must be of type dict. If not a TypeError will be raised.

    :db: Session to the database.
    :clazz: Class of which an instance should be loaded.
    :item_id: ID of the item which should be loaded.
    :values: Dictionary of values used for initialisation.
    :returns: Instance of clazz
    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))
    if not isinstance(item_id, int):
        raise TypeError("item_id must be called with a value of type {}".format(int))
    if not isinstance(values, dict):
        raise TypeError("Create must be called with a values of type {}".format(dict))
    factory = clazz.get_factory(db)
    try:
        instance = factory.load(item_id)
    except sa.orm.exc.NoResultFound:
        raise NotFound()
    instance.set_values(values)
    return instance


def _delete(db, clazz, item_id):
    """Will delete a instance of `clazz`. The instance will be removed
    from the database.

    .. seealso::

        `create` method of the specific factory of `clazz`

    `clazz` must be a subclass of :class:`BaseItem`. If not a TypeError
    will be raised.
    `item_id` must be of type integer. If not a TypeError will be raised.

    :db: Session to the database.
    :clazz: Class of which an instance should be loaded.
    :item_id: ID of the item which should be loaded.
    :returns: Instance of clazz
    """
    factory = clazz.get_factory(db)
    try:
        instance = factory.load(item_id)
    except sa.orm.exc.NoResultFound:
        raise NotFound()
    db.delete(instance)
