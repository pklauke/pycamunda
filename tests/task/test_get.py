# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_task = pycamunda.task.Get(url=engine_url, id_='anId')

    assert get_task.url == engine_url + '/task/anId'
    assert get_task.query_parameters() == {}
    assert get_task.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.Task.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_task = pycamunda.task.Get(url=engine_url, id_='anId')
    get_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_task = pycamunda.task.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.task.Task', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_task = pycamunda.task.Get(url=engine_url, id_='anId')
    get_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat')
def test_get_returns_task(engine_url):
    get_task = pycamunda.task.Get(url=engine_url, id_='anId')
    task = get_task()

    assert isinstance(task, pycamunda.task.Task)
