# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.deployment
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_delete_params(engine_url):
    delete_deployment = pycamunda.deployment.Delete(
        url=engine_url, id_='anId', cascade=True, skip_custom_listeners=True, skip_io_mappings=True
    )

    assert delete_deployment.url == engine_url + '/deployment/anId'
    assert delete_deployment.query_parameters() == {
        'cascade': True, 'skipCustomListeners': True, 'skipIoMappings': True
    }
    assert delete_deployment.body_parameters() == {}


@unittest.mock.patch('requests.delete')
def test_get_calls_requests(mock, engine_url):
    delete_deployment = pycamunda.deployment.Delete(url=engine_url, id_='anId')
    delete_deployment()

    assert mock.called


@unittest.mock.patch('requests.delete', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    delete_deployment = pycamunda.deployment.Delete(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_deployment()


@unittest.mock.patch('requests.delete', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    delete_deployment = pycamunda.deployment.Delete(url=engine_url, id_='anId')
    delete_deployment()

    assert mock.called


@unittest.mock.patch('requests.delete', unittest.mock.MagicMock())
def test_get_returns_none(engine_url):
    delete_deployment = pycamunda.deployment.Delete(url=engine_url, id_='anId')
    result = delete_deployment()

    assert result is None
