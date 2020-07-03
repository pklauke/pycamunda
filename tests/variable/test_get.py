# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_variables = pycamunda.variable.Get(url=engine_url, id_='anId')

    assert get_variables.url == engine_url + '/variable-instance/anId'
    assert get_variables.query_parameters() == {'deserializeValue': False}
    assert get_variables.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_variables = pycamunda.variable.Get(url=engine_url, id_='anId')
    get_variables()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_variables = pycamunda.variable.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_variables()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.variable.VariableInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_variables = pycamunda.variable.Get(url=engine_url, id_='anId')
    get_variables()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_variableinstance(engine_url):
    get_variable = pycamunda.variable.Get(url=engine_url, id_='anId')
    variable = get_variable()

    assert isinstance(variable, pycamunda.variable.VariableInstance)
