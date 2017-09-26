#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from ringo_core.lib.db import init_db


@pytest.fixture(scope='session')
def dbmodel(request, engine):
    init_db(engine)


@pytest.fixture()
def db(request, dbmodel, dbsession):
    return dbsession
