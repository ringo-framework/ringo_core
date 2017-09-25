#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic CRUD API"""
from ringo_core.model.base import BaseItem


def create(db, clazz, values):
    """Will return a new instance of the given class. The new instance
    will created by the specific factory of the clazz initiated
    with the given values (If the factory makes use of the values).

    `db` session to the database.
    `clazz` must be a subclass of :class:`BaseItem`. If not a TypeError
    will be raised.
    `values` must be if type dict. If not a TypeError will be raised.

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


def read(db, clazz, item_id):
    """TODO: Docstring for read.

    :clazz: TODO
    :item_id: TODO
    :returns: TODO

    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))
    if not isinstance(item_id, int):
        raise TypeError("item_id must be called with a value of type {}".format(int))
    factory = clazz.get_factory(db)
    instance = factory.load(item_id)
    return instance


def update(db, clazz, item_id, values):
    """
    :clazz: TODO
    :item_id: TODO
    :returns: TODO
    """
    if not issubclass(clazz, BaseItem):
        raise TypeError("Create must be called with a clazz of type {}".format(BaseItem))
    if not isinstance(item_id, int):
        raise TypeError("item_id must be called with a value of type {}".format(int))
    if not isinstance(values, dict):
        raise TypeError("Create must be called with a values of type {}".format(dict))
    factory = clazz.get_factory(db)
    instance = factory.load(item_id)
    instance.set_values(values)
    return instance


def delete(db, clazz, item_id):
    """TODO: Docstring for delete.

    :db: TODO
    :clazz: TODO
    :item_id: TODO
    :returns: TODO

    """
    factory = clazz.get_factory(db)
    instance = factory.load(item_id)
    db.delete(instance)
