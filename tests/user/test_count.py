# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_params):
    count_users = pycamunda.user.Count(url=engine_url, **count_input)

    assert count_users.url == engine_url + '/user/count'
    assert count_users.body_parameters() == {}
    assert count_users.query_parameters() == count_params


@unittest.mock.patch('requests.get')
def test_count_calls_requests(mock, engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    count_users()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_users()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    with pytest.raises(KeyError):
        count_users()

    assert mock.called


@unittest.mock.patch('requests.get', count_response_mock)
def test_count_returns_int(engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    count = count_users()

    assert isinstance(count, int)
