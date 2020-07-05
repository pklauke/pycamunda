# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url):
    create_filter = pycamunda.filter.Create(url=engine_url, name='aName', owner='anOwner')

    assert create_filter.url == engine_url + '/filter/create'
    assert create_filter.query_parameters() == {}
    assert create_filter.body_parameters() == {
        'name': 'aName', 'owner': 'anOwner', 'query': {}, 'resourceType': 'Task'
    }


@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url):
    create_filter = pycamunda.filter.Create(url=engine_url, name='aName', owner='anOwner')
    create_filter()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url):
    create_filter = pycamunda.filter.Create(url=engine_url, name='aName', owner='anOwner')
    with pytest.raises(pycamunda.PyCamundaException):
        create_filter()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.filter.Filter')
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url):
    create_filter = pycamunda.filter.Create(url=engine_url, name='aName', owner='anOwner')
    create_filter()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_returns_filter(engine_url):
    create_filter = pycamunda.filter.Create(url=engine_url, name='aName', owner='anOwner')
    filter_ = create_filter()

    assert isinstance(filter_, pycamunda.filter.Filter)
