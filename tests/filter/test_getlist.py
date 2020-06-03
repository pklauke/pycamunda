# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_filters = pycamunda.filter.GetList(url=engine_url, **getlist_input)

    assert get_filters.url == engine_url + '/filter'
    assert get_filters.query_parameters() == getlist_output
    assert get_filters.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_getlist_calls_requests(mock, engine_url):
    get_filters = pycamunda.filter.GetList(url=engine_url)
    get_filters()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_filters = pycamunda.filter.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_filters()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.filter.Filter', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_filters = pycamunda.filter.GetList(url=engine_url)
    get_filters()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.filter.Filter', unittest.mock.MagicMock())
def test_getlist_returns_filter_tuple(engine_url):
    get_filters = pycamunda.filter.GetList(url=engine_url)
    filters = get_filters()

    assert isinstance(filters, tuple)
    assert all(isinstance(filter_, pycamunda.filter.Filter) for filter_ in filters)
