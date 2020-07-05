# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.signal
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_eventall_params(engine_url):
    event = pycamunda.signal.EventAll(
        url=engine_url, name='aName', tenant_id='aTenantId', without_tenant_id=True
    )

    assert event.url == engine_url + '/signal'
    assert event.query_parameters() == {}
    assert event.body_parameters() == {
        'name': 'aName',
        'tenantId': 'aTenantId',
        'withoutTenantId': True,
        'variables': {}
    }


def test_eventall_variables_params(engine_url):
    event = pycamunda.signal.EventAll(url=engine_url, name='aName')
    event.add_variable(name='aName1', value='aValue1', type_='String', value_info={})

    assert event.body_parameters()['variables'] == {
        'aName1': {'value': 'aValue1', 'type': 'String', 'valueInfo': {}}
    }


@unittest.mock.patch('requests.Session.request')
def test_eventall_calls_requests(mock, engine_url):
    event = pycamunda.signal.EventAll(url=engine_url, name='aName')
    event()

    assert mock.called
    assert mock.call_args[1]['method'] == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_eventall_raises_pycamunda_exception(engine_url):
    event = pycamunda.signal.EventAll(url=engine_url, name='aName')
    with pytest.raises(pycamunda.PyCamundaException):
        event()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_eventall_raises_for_status(mock, engine_url):
    event = pycamunda.signal.EventAll(url=engine_url, name='aName')
    event()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_eventall_returns_none(engine_url):
    event = pycamunda.signal.EventAll(url=engine_url, name='aName')
    result = event()

    assert result is None


def test_eventsingle_params(engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')

    assert event.url == engine_url + '/signal'
    assert event.query_parameters() == {}
    assert event.body_parameters() == {
        'name': 'aName',
        'executionId': 'anExecutionId',
        'variables': {}
    }


def test_eventsingle_variables_params(engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')
    event.add_variable(name='aName1', value='aValue1', type_='String', value_info={})

    assert event.body_parameters()['variables'] == {
        'aName1': {'value': 'aValue1', 'type': 'String', 'valueInfo': {}}
    }


@unittest.mock.patch('requests.Session.request')
def test_eventsingle_calls_requests(mock, engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')
    event()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_eventsingle_raises_pycamunda_exception(engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')
    with pytest.raises(pycamunda.PyCamundaException):
        event()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_eventsingle_raises_for_status(mock, engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')
    event()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_eventsingle_returns_none(engine_url):
    event = pycamunda.signal.EventSingle(url=engine_url, name='aName', execution_id='anExecutionId')
    result = event()

    assert result is None
