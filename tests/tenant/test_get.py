# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_tenant = pycamunda.tenant.Get(url=engine_url, id_='aTenant')

    assert get_tenant.url == engine_url + '/tenant/aTenant'
    assert get_tenant.query_parameters() == {}
    assert get_tenant.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_tenant = pycamunda.tenant.Get(url=engine_url, id_='aTenant')
    get_tenant()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_tenant = pycamunda.tenant.Get(url=engine_url, id_='aTenant')
    with pytest.raises(pycamunda.PyCamundaException):
        get_tenant()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.tenant.Tenant', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_tenant = pycamunda.tenant.Get(url=engine_url, id_='aTenant')
    get_tenant()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_tenant(engine_url):
    get_tenant = pycamunda.tenant.Get(url=engine_url, id_='aTenant')
    tenant = get_tenant()

    assert isinstance(tenant, pycamunda.tenant.Tenant)
