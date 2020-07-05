# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_delete_params(engine_url):
    delete_definition = pycamunda.processdef.Delete(
        url=engine_url, id_='anId', cascade=True, skip_custom_listeners=True, skip_io_mappings=True
    )

    assert delete_definition.url == engine_url + '/process-definition/anId'
    assert delete_definition.query_parameters() == {
        'cascade': True, 'skipCustomListeners': True, 'skipIoMappings': True
    }
    assert delete_definition.body_parameters() == {}


def test_delete_path(engine_url):
    delete_definition_id = pycamunda.processdef.Delete(url=engine_url, id_='anId')
    delete_definition_key = pycamunda.processdef.Delete(url=engine_url, key='aKey')
    delete_definition_tenant = pycamunda.processdef.Delete(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert delete_definition_id.url == engine_url + '/process-definition/anId'
    assert delete_definition_key.url == engine_url + '/process-definition/key/aKey'
    assert delete_definition_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                        '/tenant-id/aTenantId'


@unittest.mock.patch('requests.Session.request')
def test_delete_calls_requests(mock, engine_url):
    delete_definition = pycamunda.processdef.Delete(url=engine_url, id_='anId')
    delete_definition()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url):
    delete_definition = pycamunda.processdef.Delete(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_definition()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url):
    delete_definition = pycamunda.processdef.Delete(url=engine_url, id_='anId')
    delete_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_delete_returns_none(engine_url):
    delete_definition = pycamunda.processdef.Delete(url=engine_url, id_='anId')
    result = delete_definition()

    assert result is None
