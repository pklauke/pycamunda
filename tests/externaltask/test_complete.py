# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_complete_params(engine_url):
    complete_task = pycamunda.externaltask.Complete(url=engine_url, worker_id='1', id_='anId')
    complete_task.add_variable(name='aVar', value='aVal', type_='String', value_info={})
    complete_task.add_local_variable(
        name='aLocalVar', value='aLocalVal', type_='String', value_info={}
    )

    assert complete_task.url == engine_url + '/external-task/anId/complete'
    assert complete_task.query_parameters() == {}
    assert complete_task.body_parameters() == {
        'workerId': '1',
        'variables': {'aVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}}},
        'localVariables': {'aLocalVar': {'value': 'aLocalVal', 'type': 'String', 'valueInfo': {}}}
    }


@unittest.mock.patch('requests.Session.request')
def test_complete_calls_requests(mock, engine_url):
    complete_task = pycamunda.externaltask.Complete(url=engine_url, worker_id='1', id_='anId')
    complete_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_complete_raises_pycamunda_exception(engine_url):
    complete_task = pycamunda.externaltask.Complete(url=engine_url, worker_id='1', id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        complete_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_complete_raises_for_status(mock, engine_url):
    complete_task = pycamunda.externaltask.Complete(url=engine_url, worker_id='1', id_='anId')
    complete_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_complete_returns_none(engine_url):
    complete_task = pycamunda.externaltask.Complete(url=engine_url, worker_id='1', id_='anId')
    result = complete_task()

    assert result is None
