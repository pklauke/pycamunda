# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url, task_input, task_output):
    create_task = pycamunda.task.Create(url=engine_url, id_='anId', **task_input)

    assert create_task.url == engine_url + '/task/create'
    assert create_task.query_parameters() == {}
    assert create_task.body_parameters() == {'id': 'anId', **task_output}


@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url, task_input):
    create_task = pycamunda.task.Create(url=engine_url, id_='anId', **task_input)
    create_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url, task_input):
    create_task = pycamunda.task.Create(url=engine_url, id_='anId', **task_input)
    with pytest.raises(pycamunda.PyCamundaException):
        create_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url, task_input):
    create_task = pycamunda.task.Create(url=engine_url, id_='anId', **task_input)
    create_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_returns_none(engine_url, task_input):
    create_task = pycamunda.task.Create(url=engine_url, id_='anId', **task_input)
    result = create_task()

    assert result is None
