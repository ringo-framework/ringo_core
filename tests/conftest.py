#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from ringo_core.lib.security import generate_password
from ringo_core.lib.db import init_db

# Initialise a SQLite Database for doctests. Doctests can not use the
# fixtures and contexts of py.test. So default sqlite db in memory is
# not present at the time the doctests are executed. As a workaround we
# create a temporary sqlite database on "make doctests". This call
# initialises this database.
init_db()


@pytest.fixture(scope='session')
def dbmodel(request, engine):
    init_db(engine)


@pytest.fixture()
def db(request, dbmodel, dbsession):
    return dbsession


@pytest.fixture()
def randomstring(request):
    return generate_password
