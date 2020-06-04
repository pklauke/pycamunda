# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_executecount_params(engine_url):
    get_filter_count = pycamunda.filter.ExecuteCount(url=engine_url, id_='anId')

    assert get_filter_count.url == engine_url + '/filter/anId/count'
    assert get_filter_count.query_parameters() == {}
    assert get_filter_count.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_executecount_calls_requests(mock, engine_url):
    get_filter_count = pycamunda.filter.ExecuteCount(url=engine_url, id_='anId')
    get_filter_count()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_executecount_raises_pycamunda_exception(engine_url):
    get_filter_count = pycamunda.filter.ExecuteCount(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_filter_count()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_executecount_raises_for_status(mock, engine_url):
    get_filter_count = pycamunda.filter.ExecuteCount(url=engine_url, id_='anId')
    get_filter_count()

    assert mock.called


@unittest.mock.patch('requests.get', count_response_mock)
def test_executecount_returns_int(engine_url):
    get_filter_count = pycamunda.filter.ExecuteCount(url=engine_url, id_='anId')
    filter_ = get_filter_count()

    assert isinstance(filter_, int)
