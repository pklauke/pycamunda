# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_definition = pycamunda.processdef.Get(url=engine_url, id_='anId')

    assert get_definition.url == engine_url + '/process-definition/anId'
    assert get_definition.query_parameters() == {}
    assert get_definition.body_parameters() == {}


def test_get_path(engine_url):
    get_definition_id = pycamunda.processdef.Get(url=engine_url, id_='anId')
    get_definition_key = pycamunda.processdef.Get(url=engine_url, key='aKey')
    get_definition_tenant = pycamunda.processdef.Get(url=engine_url, key='aKey', tenant_id='aTenantId')

    assert get_definition_id.url == engine_url + '/process-definition/anId'
    assert get_definition_key.url == engine_url + '/process-definition/key/aKey'
    assert get_definition_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                     '/tenant-id/aTenantId'


@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_definition = pycamunda.processdef.Get(url=engine_url, id_='anId')
    get_definition()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_definition = pycamunda.processdef.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_definition()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ProcessDefinition', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_definition = pycamunda.processdef.Get(url=engine_url, id_='anId')
    get_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_processdefinition(engine_url):
    get_definition = pycamunda.processdef.Get(url=engine_url, id_='anId')
    process_definition = get_definition()

    assert isinstance(process_definition, pycamunda.processdef.ProcessDefinition)
