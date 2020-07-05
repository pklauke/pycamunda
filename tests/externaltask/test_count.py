# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_count_params(engine_url, getlist_input, getlist_output):
    count_tasks = pycamunda.externaltask.Count(url=engine_url, **getlist_input)

    assert count_tasks.url == engine_url + '/external-task/count'
    assert count_tasks.query_parameters() == getlist_output
    assert count_tasks.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_count_calls_requests(mock, engine_url):
    count_tasks = pycamunda.externaltask.Count(url=engine_url)
    count_tasks()

    assert mock.called
    print(mock.call_args)
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_tasks = pycamunda.externaltask.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_tasks()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_tasks = pycamunda.externaltask.Count(url=engine_url)
    count_tasks()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_count_returns_int(engine_url):
    count_tasks = pycamunda.externaltask.Count(url=engine_url)
    result = count_tasks()

    assert isinstance(result, int)
