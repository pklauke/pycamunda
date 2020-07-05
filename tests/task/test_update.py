# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url, task_input, task_output):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **task_input)

    assert update_task.url == engine_url + '/task/anId'
    assert update_task.query_parameters() == {}
    assert update_task.body_parameters() == task_output


@unittest.mock.patch('requests.Session.request')
def test_update_calls_requests(mock, engine_url, task_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **task_input)
    update_task()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url, task_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **task_input)
    with pytest.raises(pycamunda.PyCamundaException):
        update_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url, task_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **task_input)
    update_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_update_returns_none(engine_url, task_input):
    update_task = pycamunda.task.Update(url=engine_url, id_='anId', **task_input)
    result = update_task()

    assert result is None
