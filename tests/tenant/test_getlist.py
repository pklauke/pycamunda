# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, get_list_input, get_list_output):
    get_tenants = pycamunda.tenant.GetList(url=engine_url, **get_list_input)

    assert get_tenants.url == engine_url + '/tenant'
    assert get_tenants.body_parameters() == {}
    assert get_tenants.query_parameters() == get_list_output


@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests(mock, engine_url):
    get_tenants = pycamunda.tenant.GetList(url=engine_url)
    get_tenants()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_tenants = pycamunda.tenant.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_tenants()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.tenant.Tenant', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_tenants = pycamunda.tenant.GetList(url=engine_url)
    get_tenants()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getlist_returns_tenants(engine_url):
    get_tenants = pycamunda.tenant.GetList(url=engine_url, id_='anId')
    tenants = get_tenants()

    assert isinstance(tenants, tuple)
    assert all(isinstance(tenant, pycamunda.tenant.Tenant) for tenant in tenants)
