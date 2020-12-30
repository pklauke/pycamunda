# -*- coding: utf-8 -*-

import datetime as dt

import pytest

import pycamunda.base
import pycamunda.request


@pytest.fixture
def MyRequest():
    class _MyRequest(pycamunda.base.CamundaRequest):

        query_param = pycamunda.request.QueryParameter('param')
        body_param = pycamunda.request.BodyParameter('param')

        def __init__(self, url, query_param=None, body_param=None):
            super().__init__(url=url)
            self.query_param = query_param
            self.body_param = body_param

    return _MyRequest


@pytest.fixture
def date():
    return dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)


@pytest.fixture
def date_str():
    return '2020-01-01T01:01:01.000'


@pytest.fixture
def date_tz():
    date = dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
    return date.replace(tzinfo=dt.timezone.utc)


@pytest.fixture
def date_tz_str():
    return '2020-01-01T01:01:01.000+0000'
