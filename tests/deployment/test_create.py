# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.deployment
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url, create_input, create_output):
    create_deployment = pycamunda.deployment.Create(url=engine_url, **create_input)

    assert create_deployment.url == engine_url + '/deployment/create'
    assert create_deployment.query_parameters() == {}
    assert create_deployment.body_parameters() == create_output


@unittest.mock.patch('requests.Session.request')
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_create_calls_requests(mock, engine_url):
    create_deployment = pycamunda.deployment.Create(url=engine_url, name='aName', source='aSource')
    create_deployment.add_resource(file='NotARealFile')
    create_deployment()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url):
    create_deployment = pycamunda.deployment.Create(url=engine_url, name='aName', source='aSource')
    create_deployment.add_resource(file='NotARealFile')
    with pytest.raises(pycamunda.PyCamundaException):
        create_deployment()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch(
    'pycamunda.deployment.DeploymentWithDefinitions.load', unittest.mock.MagicMock()
)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url):
    create_deployment = pycamunda.deployment.Create(url=engine_url, name='aName', source='aSource')
    create_deployment.add_resource(file='NotARealFile')
    create_deployment()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_create_returns_deployment_with_definitions(engine_url):
    create_deployment = pycamunda.deployment.Create(url=engine_url, name='aName', source='aSource')
    create_deployment.add_resource(file='NotARealFile')
    result = create_deployment()

    assert isinstance(result, pycamunda.deployment.DeploymentWithDefinitions)
