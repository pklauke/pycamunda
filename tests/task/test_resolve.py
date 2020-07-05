# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_resolve_params(engine_url):
    resolve_task = pycamunda.task.Resolve(url=engine_url, id_='anId')
    resolve_task.add_variable(name='aVar', value='aVal', type_='String', value_info='')

    assert resolve_task.url == engine_url + '/task/anId/resolve'
    assert resolve_task.query_parameters() == {}
    assert resolve_task.body_parameters() == {
        'variables': {'aVar': {'value': 'aVal', 'type': 'String', 'valueInfo': ''}}
    }


@unittest.mock.patch('requests.Session.request')
def test_resolve_calls_requests(mock, engine_url):
    resolve_task = pycamunda.task.Resolve(url=engine_url, id_='anId')
    resolve_task()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_resolve_raises_pycamunda_exception(engine_url):
    resolve_task = pycamunda.task.Resolve(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        resolve_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_resolve_raises_for_status(mock, engine_url):
    resolve_task = pycamunda.task.Resolve(url=engine_url, id_='anId')
    resolve_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_resolve_returns_none(engine_url):
    resolve_task = pycamunda.task.Resolve(url=engine_url, id_='anId')
    result = resolve_task()

    assert result is None
