# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_variables = pycamunda.variable.GetList(url=engine_url, **getlist_input)

    assert get_variables.url == engine_url + '/variable-instance'
    assert get_variables.query_parameters() == getlist_output
    assert get_variables.body_parameters() == {}


def test_getlist_params_add_equal_value_filter(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables.add_equal_value_filter(name='aName', value=1)

    assert get_variables.query_parameters()['variableValues'] == 'aName_eq_1'


def test_getlist_params_add_not_equal_value_filter(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables.add_not_equal_value_filter(name='aName', value=1)

    assert get_variables.query_parameters()['variableValues'] == 'aName_neq_1'


def test_getlist_params_add_greater_than_value_filter(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables.add_greater_than_value_filter(name='aName', value=1)

    assert get_variables.query_parameters()['variableValues'] == 'aName_gt_1'


def test_getlist_params_add_less_than_value_filter(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables.add_less_than_value_filter(name='aName', value=1)

    assert get_variables.query_parameters()['variableValues'] == 'aName_lt_1'


def test_getlist_params_add_like_value_filter(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables.add_like_value_filter(name='aName', value='aValu')

    assert get_variables.query_parameters()['variableValues'] == 'aName_like_aValu'


@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests(mock, engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables()

    assert mock.called
    assert mock.call_args[1]['method'] == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_variables()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.variable.VariableInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    get_variables()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getlist_returns_variableinstances(engine_url):
    get_variables = pycamunda.variable.GetList(url=engine_url)
    variables = get_variables()

    assert isinstance(variables, tuple)
    assert all(isinstance(variable, pycamunda.variable.VariableInstance) for variable in variables)
