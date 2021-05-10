# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_variablesmodify_params(engine_url):
    modify_vars = pycamunda.processinst.VariablesModify(
        url=engine_url, process_instance_id='anId', deletions=['aVar']
    )
    modify_vars.add_variable(name='anotherVar', value='aVal', type_='String', value_info={})

    assert modify_vars.url == engine_url + '/process-instance/anId/variables'
    assert modify_vars.query_parameters() == {}
    assert modify_vars.body_parameters() == {
        'modifications': {'anotherVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}}},
        'deletions': ['aVar']
    }


@unittest.mock.patch('requests.Session.request')
def test_variablesmodify_calls_requests(mock, engine_url):
    modify_vars = pycamunda.processinst.VariablesModify(url=engine_url, process_instance_id='anId')
    modify_vars()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_variablesmodify_raises_pycamunda_exception(engine_url):
    modify_vars = pycamunda.processinst.VariablesModify(url=engine_url, process_instance_id='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        modify_vars()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_variablesmodify_raises_for_status(mock, engine_url):
    modify_vars = pycamunda.processinst.VariablesModify(url=engine_url, process_instance_id='anId')
    modify_vars()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_variablesmodify_returns_none(engine_url):
    modify_vars = pycamunda.processinst.VariablesModify(url=engine_url, process_instance_id='anId')
    result = modify_vars()

    assert result is None
