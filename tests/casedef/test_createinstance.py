# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.casedef
import pycamunda.caseinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_createinstance_params(engine_url):
    create_instance = pycamunda.casedef.CreateInstance(
        url=engine_url,
        id_='anId',
        business_key='aBusinessKey'
    )
    create_instance.add_variable(name='aVar', value='aVal', type_='aType', value_info='anInfo')

    assert create_instance.url == engine_url + '/case-definition/anId/create'
    assert create_instance.query_parameters() == {}
    assert create_instance.body_parameters() == {
        'businessKey': 'aBusinessKey',
        'variables': {'aVar': {'value': 'aVal', 'type': 'aType', 'valueInfo': 'anInfo'}}
    }


def test_createinstance_path(engine_url):
    create_instance_id = pycamunda.casedef.CreateInstance(
        url=engine_url, id_='anId'
    )
    create_instance_key = pycamunda.casedef.CreateInstance(
        url=engine_url, key='aKey'
    )
    create_instance_tenant = pycamunda.casedef.CreateInstance(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert create_instance_id.url == engine_url + '/case-definition/anId/create'
    assert create_instance_key.url == engine_url + '/case-definition/key/aKey/create'
    assert create_instance_tenant.url == engine_url + '/case-definition/key/aKey' \
                                                      '/tenant-id/aTenantId/create'


@unittest.mock.patch('requests.Session.request')
def test_createinstance_calls_requests(mock, engine_url):
    create_instance = pycamunda.casedef.CreateInstance(url=engine_url, id_='anId')
    create_instance()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_createinstance_raises_pycamunda_exception(engine_url):
    create_instance = pycamunda.casedef.CreateInstance(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        create_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.caseinst.CaseInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_createinstance_raises_for_status(mock, engine_url):
    create_instance = pycamunda.casedef.CreateInstance(url=engine_url, id_='anId')
    create_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_createinstance_returns_caseinstance(engine_url):
    create_instance = pycamunda.casedef.CreateInstance(url=engine_url, id_='anId')
    instance = create_instance()

    assert isinstance(instance, pycamunda.caseinst.CaseInstance)
