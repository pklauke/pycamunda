# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_output):
    get_count = pycamunda.authorization.Count(url=engine_url, **count_input)

    assert get_count.url == engine_url + '/authorization/count'
    assert get_count.query_parameters() == count_output
    assert get_count.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_count_calls_requests(mock, engine_url):
    get_count = pycamunda.authorization.Count(url=engine_url)
    get_count()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    get_count = pycamunda.authorization.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_count()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    get_count = pycamunda.authorization.Count(url=engine_url)
    get_count()

    assert mock.called


@unittest.mock.patch('requests.Session.request', count_response_mock)
def test_count_returns_authorizations(engine_url):
    get_count = pycamunda.authorization.Count(url=engine_url)
    count = get_count()

    assert isinstance(count, int)
