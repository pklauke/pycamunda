# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_localvariablesget_params(engine_url):
    get_var = pycamunda.task.LocalVariablesGet(
        url=engine_url, task_id='anId', var_name='aVar', deserialize_value=True
    )

    assert get_var.url == engine_url + '/task/anId/localVariables/aVar'
    assert get_var.query_parameters() == {'deserializeValue': True}
    assert get_var.body_parameters() == {}


def test_localvariablesget_binary_params(engine_url):
    get_var = pycamunda.task.LocalVariablesGet(
        url=engine_url, task_id='anId', var_name='aVar', deserialize_value=True, binary=True
    )

    assert get_var.url == engine_url + '/task/anId/localVariables/aVar/data'


@unittest.mock.patch('requests.Session.request')
def test_localvariablesget_calls_requests(mock, engine_url):
    get_var = pycamunda.task.LocalVariablesGet(url=engine_url, task_id='anId', var_name='aVar')
    get_var()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_localvariablesget_raises_pycamunda_exception(engine_url):
    get_var = pycamunda.task.LocalVariablesGet(url=engine_url, task_id='anId', var_name='aVar')
    with pytest.raises(pycamunda.PyCamundaException):
        get_var()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.variable.Variable', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_localvariablesget_raises_for_status(mock, engine_url):
    get_var = pycamunda.task.LocalVariablesGet(url=engine_url, task_id='anId', var_name='aVar')
    get_var()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_localvariablesget_returns_variable(engine_url):
    get_var = pycamunda.task.LocalVariablesGet(url=engine_url, task_id='anId', var_name='aVar')
    variable = get_var()

    assert isinstance(variable, pycamunda.variable.Variable)
