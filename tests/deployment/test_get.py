# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.deployment
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_deployment = pycamunda.deployment.Get(url=engine_url, id_='anId')

    assert get_deployment.url == engine_url + '/deployment/anId'
    assert get_deployment.query_parameters() == {}
    assert get_deployment.body_parameters() == {}


@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_deployment = pycamunda.deployment.Get(url=engine_url, id_='anId')
    get_deployment()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_deployment = pycamunda.deployment.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_deployment()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.deployment.Deployment', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_deployment = pycamunda.deployment.Get(url=engine_url, id_='anId')
    get_deployment()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat')
def test_get_returns_response_content(engine_url):
    get_deployment = pycamunda.deployment.Get(url=engine_url, id_='anId')
    deployment = get_deployment()

    assert isinstance(deployment, pycamunda.deployment.Deployment)
