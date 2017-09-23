#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from ringo_core.model.base import create_model


@pytest.fixture(scope='session')
def dbmodel(request, engine):
    create_model(engine)


@pytest.fixture()
def db(request, dbmodel, dbsession):
    return dbsession
