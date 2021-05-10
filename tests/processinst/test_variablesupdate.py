# -*- coding: utf-8 -*-

import io
import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_variablesupdate_params(engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value='aVal',
        type_='String',
        value_info={}
    )

    assert update_var.url == engine_url + '/process-instance/anId/variables/aVar'
    assert update_var.query_parameters() == {}
    assert update_var.body_parameters() == {'value': 'aVal', 'type': 'String', 'valueInfo': {}}


def test_variablesupdate_binary_params(engine_url):
    update_var1 = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value=io.StringIO('myfile'),
        type_='File'
    )
    update_var2 = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value=io.StringIO('myfile'),
        type_='Bytes'
    )

    assert update_var1.url == engine_url + '/process-instance/anId/variables/aVar/data'
    assert update_var2.url == engine_url + '/process-instance/anId/variables/aVar/data'
    assert update_var1.query_parameters() == {}
    assert update_var2.query_parameters() == {}
    assert update_var1.body_parameters() == {'valueType': 'File'}
    assert update_var2.body_parameters() == {'valueType': 'Bytes'}


@unittest.mock.patch('requests.Session.request')
def test_variablesupdate_calls_requests(mock, engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value='aVal',
        type_='String',
        value_info={}
    )
    update_var()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request')
def test_variablesupdate_binary_calls_requests(mock, engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value=io.StringIO('myfile'),
        type_='Bytes'
    )
    update_var()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_variablesupdate_raises_pycamunda_exception(engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value='aVal',
        type_='String',
        value_info={}
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_var()


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_variablesupdate_binary_raises_pycamunda_exception(engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value=io.StringIO('myfile'),
        type_='Bytes'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_var()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_variablesupdate_raises_for_status(mock, engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value='aVal',
        type_='String',
        value_info={}
    )
    update_var()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_variablesupdate_returns_none(engine_url):
    update_var = pycamunda.processinst.VariablesUpdate(
        url=engine_url,
        process_instance_id='anId',
        var_name='aVar',
        value='aVal',
        type_='String',
        value_info={}
    )
    result = update_var()

    assert result is None
