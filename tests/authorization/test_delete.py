# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_delete_params(engine_url):
    delete_authorization = pycamunda.authorization.Delete(url=engine_url, id_='anId')

    assert delete_authorization.url == engine_url + '/authorization/anId'
    assert delete_authorization.query_parameters() == {}
    assert delete_authorization.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_delete_calls_requests(mock, engine_url):
    delete_authorization = pycamunda.authorization.Delete(url=engine_url, id_='anId')
    delete_authorization()

    assert mock.called
    assert mock.call_args[1]['method'] == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url):
    delete_authorization = pycamunda.authorization.Delete(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_authorization()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url, create_input):
    delete_authorization = pycamunda.authorization.Delete(url=engine_url, id_='anId')
    delete_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_delete_returns_none(engine_url):
    delete_authorization = pycamunda.authorization.Delete(url=engine_url, id_='anId')
    result = delete_authorization()

    assert result is None
