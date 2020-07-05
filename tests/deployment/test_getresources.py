# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.deployment
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getresources_params(engine_url):
    get_resources = pycamunda.deployment.GetResources(url=engine_url, id_='anId')

    assert get_resources.url == engine_url + '/deployment/anId/resources'
    assert get_resources.query_parameters() == {}
    assert get_resources.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_getresources_calls_requests(mock, engine_url):
    get_resources = pycamunda.deployment.GetResources(url=engine_url, id_='anId')
    get_resources()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getresources_raises_pycamunda_exception(engine_url):
    get_resources = pycamunda.deployment.GetResources(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_resources()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
@unittest.mock.patch('pycamunda.deployment.Resource', unittest.mock.MagicMock())
def test_getresources_raises_for_status(mock, engine_url):
    get_resources = pycamunda.deployment.GetResources(url=engine_url, id_='anId')
    get_resources()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.deployment.Resource', unittest.mock.MagicMock())
def test_getresources_returns_resources(engine_url):
    get_resources = pycamunda.deployment.GetResources(url=engine_url, id_='anId')
    resources = get_resources()

    assert isinstance(resources, tuple)
    assert all(isinstance(resource, pycamunda.deployment.Resource) for resource in resources)
