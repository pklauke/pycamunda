# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_filter = pycamunda.filter.Get(url=engine_url, id_='anId', item_count=True)

    assert get_filter.url == engine_url + '/filter/anId'
    assert get_filter.query_parameters() == {'itemCount': True}
    assert get_filter.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_get_calls_requests(mock, engine_url):
    get_filter = pycamunda.filter.Get(url=engine_url, id_='anId', item_count=True)
    get_filter()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_filter = pycamunda.filter.Get(url=engine_url, id_='anId', item_count=True)
    with pytest.raises(pycamunda.PyCamundaException):
        get_filter()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.filter.Filter', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_filter = pycamunda.filter.Get(url=engine_url, id_='anId', item_count=True)
    get_filter()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
def test_get_returns_filter(engine_url):
    get_filter = pycamunda.filter.Get(url=engine_url, id_='anId', item_count=True)
    filter_ = get_filter()

    assert isinstance(filter_, pycamunda.filter.Filter)
