# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_unclaim_params(engine_url):
    unclaim_task = pycamunda.task.Unclaim(url=engine_url, id_='anId')

    assert unclaim_task.url == engine_url + '/task/anId/unclaim'
    assert unclaim_task.query_parameters() == {}
    assert unclaim_task.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_unclaim_calls_requests(mock, engine_url):
    unclaim_task = pycamunda.task.Unclaim(url=engine_url, id_='anId')
    unclaim_task()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_unclaim_raises_pycamunda_exception(engine_url):
    unclaim_task = pycamunda.task.Unclaim(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        unclaim_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_unclaim_raises_for_status(mock, engine_url):
    unclaim_task = pycamunda.task.Unclaim(url=engine_url, id_='anId')
    unclaim_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_unclaim_returns_none(engine_url):
    unclaim_task = pycamunda.task.Unclaim(url=engine_url, id_='anId')
    result = unclaim_task()

    assert result is None
