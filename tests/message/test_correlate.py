# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.message
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_correlatesingle_params(engine_url, correlate_input, correlate_output):
    correlate = pycamunda.message.CorrelateSingle(
        url=engine_url, message_name='aMessageName', **correlate_input
    )

    assert correlate.url == engine_url + '/message'
    assert correlate.query_parameters() == {}
    assert correlate.body_parameters() == {
        'messageName': 'aMessageName',
        **correlate_output,
        'all': False
    }


def test_correlatesingle_method_params(engine_url):
    correlate = pycamunda.message.CorrelateSingle(url=engine_url, message_name='aMessageName')
    correlate.add_process_variable(name='aName1', value='aValue1', type_='String', value_info={})
    correlate.add_local_process_variable(
        name='aName2', value='aValue2', type_='String', value_info={}
    )
    correlate.add_correlation_key(name='aName3', value='aValue3', type_='String')
    correlate.add_local_correlation_key(name='aName4', value='aValue4', type_='String')

    params = correlate.body_parameters()
    assert params['processVariables'] == {
        'aName1': {'value': 'aValue1', 'type': 'String', 'valueInfo': {}}
    }
    assert params['processVariablesLocal'] == {
        'aName2': {'value': 'aValue2', 'type': 'String', 'valueInfo': {}}
    }
    assert params['correlationKeys'] == {
        'aName3': {'value': 'aValue3', 'type': 'String'}
    }
    assert params['localCorrelationKeys'] == {
        'aName4': {'value': 'aValue4', 'type': 'String'}
    }


@unittest.mock.patch('pycamunda.message.MessageCorrelationResult', unittest.mock.MagicMock())
@unittest.mock.patch('requests.post')
def test_correlatesingle_calls_requests(mock, engine_url):
    correlate = pycamunda.message.CorrelateSingle(url=engine_url, message_name='aMessageName')
    correlate()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_correlatesingle_raises_pycamunda_exception(engine_url):
    correlate = pycamunda.message.CorrelateSingle(url=engine_url, message_name='aMessageName')
    with pytest.raises(pycamunda.PyCamundaException):
        correlate()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.message.MessageCorrelationResult', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_correlatesingle_raises_for_status(mock, engine_url):
    correlate = pycamunda.message.CorrelateSingle(url=engine_url, message_name='aMessageName')
    correlate()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.message.ResultType', unittest.mock.MagicMock())
def test_correlatesingle_returns_messagecorrelationresult(engine_url):
    correlate = pycamunda.message.CorrelateSingle(url=engine_url, message_name='aMessageName')
    result = correlate()

    assert isinstance(result, pycamunda.message.MessageCorrelationResult)
