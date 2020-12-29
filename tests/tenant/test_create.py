# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url):
    create_tenant = pycamunda.tenant.Create(url=engine_url, id_='aTenant', name='a tenant')

    assert create_tenant.url == engine_url + '/tenant/create'
    assert create_tenant.query_parameters() == {}
    assert create_tenant.body_parameters() == {'id': 'aTenant', 'name': 'a tenant'}


@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url):
    create_tenant = pycamunda.tenant.Create(url=engine_url, id_='aTenant', name='a tenant')
    create_tenant()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url):
    create_tenant = pycamunda.tenant.Create(url=engine_url, id_='aTenant', name='a tenant')
    with pytest.raises(pycamunda.PyCamundaException):
        create_tenant()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url):
    create_tenant = pycamunda.tenant.Create(url=engine_url, id_='aTenant', name='a tenant')
    create_tenant()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_returns_none(engine_url):
    create_tenant = pycamunda.tenant.Create(url=engine_url, id_='aTenant', name='a tenant')
    result = create_tenant()

    assert result is None
