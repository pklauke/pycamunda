# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_localvariablesupdate_params(engine_url):
    update_var = pycamunda.task.LocalVariablesUpdate(
        url=engine_url, task_id='anId', var_name='aVar', value='aVal', type_='String', value_info={}
    )

    assert update_var.url == engine_url + '/task/anId/localVariables/aVar'
    assert update_var.query_parameters() == {}
    assert update_var.body_parameters() == {'value': 'aVal', 'type': 'String', 'valueInfo': {}}


@unittest.mock.patch('requests.put')
def test_localvariablesupdate_calls_requests(mock, engine_url):
    update_var = pycamunda.task.LocalVariablesUpdate(
        url=engine_url, task_id='anId', var_name='aVar', value='aVal', type_='String', value_info={}
    )
    update_var()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_localvariablesupdate_raises_pycamunda_exception(engine_url):
    update_var = pycamunda.task.LocalVariablesUpdate(
        url=engine_url, task_id='anId', var_name='aVar', value='aVal', type_='String', value_info={}
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_var()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_localvariablesupdate_raises_for_status(mock, engine_url):
    update_var = pycamunda.task.LocalVariablesUpdate(
        url=engine_url, task_id='anId', var_name='aVar', value='aVal', type_='String', value_info={}
    )
    update_var()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_localvariablesupdate_returns_none(engine_url):
    update_var = pycamunda.task.LocalVariablesUpdate(
        url=engine_url, task_id='anId', var_name='aVar', value='aVal', type_='String', value_info={}
    )
    result = update_var()

    assert result is None
