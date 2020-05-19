# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.deployment
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_getresource_params(engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId', binary=False
    )

    assert get_resource.url == engine_url + '/deployment/anId/resources/aResourceId'
    assert get_resource.query_parameters() == {}
    assert get_resource.body_parameters() == {}


def test_getresource_binary_params(engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId', binary=True
    )

    assert get_resource.url == engine_url + '/deployment/anId/resources/aResourceId/data'
    assert get_resource.query_parameters() == {}
    assert get_resource.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_getresource_calls_requests(mock, engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId'
    )
    get_resource()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getresource_raises_pycamunda_exception(engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        get_resource()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
@unittest.mock.patch('pycamunda.deployment.Resource', unittest.mock.MagicMock())
def test_getresource_raises_for_status(mock, engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId'
    )
    get_resource()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
def test_getresources_returns_resource(engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId'
    )
    resource = get_resource()

    assert isinstance(resource, pycamunda.deployment.Resource)


@unittest.mock.patch('requests.get', response_mock)
def test_getresources_binary_returns_content(engine_url):
    get_resource = pycamunda.deployment.GetResource(
        url=engine_url, id_='anId', resource_id='aResourceId', binary=True
    )
    result = get_resource()

    assert result == response_mock().content
