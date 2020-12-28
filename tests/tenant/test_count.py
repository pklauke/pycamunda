# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_count_params(engine_url, count_input, count_output):
    count_tenants = pycamunda.tenant.Count(url=engine_url, **count_input)

    assert count_tenants.url == engine_url + '/tenant/count'
    assert count_tenants.body_parameters() == {}
    assert count_tenants.query_parameters() == count_output


@unittest.mock.patch('requests.Session.request')
def test_count_calls_requests(mock, engine_url):
    count_tenants = pycamunda.tenant.Count(url=engine_url)
    count_tenants()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_tenants = pycamunda.tenant.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_tenants()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.tenant.Tenant', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_tenants = pycamunda.tenant.Count(url=engine_url)
    count_tenants()

    assert mock.called


@unittest.mock.patch('requests.Session.request', count_response_mock)
def test_count_returns_integer(engine_url):
    count_tenants = pycamunda.tenant.Count(url=engine_url, id_='anId')
    tenants = count_tenants()

    assert isinstance(tenants, int)
