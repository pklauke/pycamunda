# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_variablesdelete_params(engine_url):
    delete_var = pycamunda.processinst.VariablesDelete(
        url=engine_url, process_instance_id='anId', var_name='aVar'
    )

    assert delete_var.url == engine_url + '/process-instance/anId/variables/aVar'
    assert delete_var.query_parameters() == {}
    assert delete_var.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_variablesdelete_calls_requests(mock, engine_url):
    delete_var = pycamunda.processinst.VariablesDelete(
        url=engine_url, process_instance_id='anId', var_name='aVar'
    )
    delete_var()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_variablesdelete_raises_pycamunda_exception(engine_url):
    delete_var = pycamunda.processinst.VariablesDelete(
        url=engine_url, process_instance_id='anId', var_name='aVar'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        delete_var()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_variablesdelete_raises_for_status(mock, engine_url):
    delete_var = pycamunda.processinst.VariablesDelete(
        url=engine_url, process_instance_id='anId', var_name='aVar'
    )
    delete_var()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_variablesdelete_returns_none(engine_url):
    delete_var = pycamunda.processinst.VariablesDelete(
        url=engine_url, process_instance_id='anId', var_name='aVar'
    )
    result = delete_var()

    assert result is None
