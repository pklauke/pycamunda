# -*- coding: utf-8 -*-

import datetime as dt
import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_activate_params(engine_url):
    activate_definition = pycamunda.processdef.Activate(
        url=engine_url,
        id_='anId',
        include_process_instances=True,
        execution_datetime=dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
    )

    assert activate_definition.url == engine_url + '/process-definition/anId/suspended'
    assert activate_definition.query_parameters() == {}
    assert activate_definition.body_parameters() == {
        'includeProcessInstances': True,
        'executionDate': '2020-01-01T01:01:01.000',
        'suspended': False
    }


def test_activate_path(engine_url):
    activate_definition_id = pycamunda.processdef.Activate(url=engine_url, id_='anId')
    activate_definition_key = pycamunda.processdef.Activate(url=engine_url, key='aKey')
    activate_definition_tenant = pycamunda.processdef.Activate(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert activate_definition_id.url == engine_url + '/process-definition/anId/suspended'
    assert activate_definition_key.url == engine_url + '/process-definition/key/aKey/suspended'
    assert activate_definition_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                          '/tenant-id/aTenantId/suspended'


@unittest.mock.patch('requests.Session.request')
def test_activate_calls_requests(mock, engine_url):
    activate_definition = pycamunda.processdef.Activate(url=engine_url, id_='anId')
    activate_definition()

    assert mock.called
    assert mock.call_args[1]['method'] == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_activate_raises_pycamunda_exception(engine_url):
    activate_definition = pycamunda.processdef.Activate(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        activate_definition()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_activate_raises_for_status(mock, engine_url):
    activate_definition = pycamunda.processdef.Activate(url=engine_url, id_='anId')
    activate_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_activate_returns_none(engine_url):
    activate_definition = pycamunda.processdef.Activate(url=engine_url, id_='anId')
    result = activate_definition()

    assert result is None


def test_suspend_params(engine_url):
    suspend_definition = pycamunda.processdef.Suspend(
        url=engine_url,
        id_='anId',
        include_process_instances=True,
        execution_datetime=dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
    )

    assert suspend_definition.url == engine_url + '/process-definition/anId/suspended'
    assert suspend_definition.query_parameters() == {}
    assert suspend_definition.body_parameters() == {
        'includeProcessInstances': True,
        'executionDate': '2020-01-01T01:01:01.000',
        'suspended': True
    }


def test_suspend_path(engine_url):
    suspend_definition_id = pycamunda.processdef.Suspend(url=engine_url, id_='anId')
    suspend_definition_key = pycamunda.processdef.Suspend(url=engine_url, key='aKey')
    suspend_definition_tenant = pycamunda.processdef.Suspend(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert suspend_definition_id.url == engine_url + '/process-definition/anId/suspended'
    assert suspend_definition_key.url == engine_url + '/process-definition/key/aKey/suspended'
    assert suspend_definition_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                          '/tenant-id/aTenantId/suspended'


@unittest.mock.patch('requests.Session.request')
def test_suspend_calls_requests(mock, engine_url):
    suspend_definition = pycamunda.processdef.Suspend(url=engine_url, id_='anId')
    suspend_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_suspend_raises_pycamunda_exception(engine_url):
    suspend_definition = pycamunda.processdef.Suspend(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        suspend_definition()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_suspend_raises_for_status(mock, engine_url):
    suspend_definition = pycamunda.processdef.Suspend(url=engine_url, id_='anId')
    suspend_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_suspend_returns_none(engine_url):
    suspend_definition = pycamunda.processdef.Suspend(url=engine_url, id_='anId')
    result = suspend_definition()

    assert result is None
