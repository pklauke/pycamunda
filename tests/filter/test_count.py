# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_output):
    count_filters = pycamunda.filter.Count(url=engine_url, **count_input)

    assert count_filters.url == engine_url + '/filter/count'
    assert count_filters.query_parameters() == count_output
    assert count_filters.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_count_calls_requests(mock, engine_url):
    count_filters = pycamunda.filter.Count(url=engine_url)
    count_filters()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_filters = pycamunda.filter.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_filters()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_filters = pycamunda.filter.Count(url=engine_url)
    count_filters()

    assert mock.called


@unittest.mock.patch('requests.Session.request', count_response_mock)
def test_count_returns_int(engine_url):
    count_filters = pycamunda.filter.Count(url=engine_url)
    result = count_filters()

    assert isinstance(result, int)
