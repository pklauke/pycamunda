# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_authorization = pycamunda.authorization.Get(url=engine_url, id_='anId')

    assert get_authorization.url == engine_url + '/authorization/anId'
    assert get_authorization.query_parameters() == {}
    assert get_authorization.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
@unittest.mock.patch('pycamunda.resource.ResourceType', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_get_calls_requests(mock, engine_url):
    get_authorization = pycamunda.authorization.Get(url=engine_url, id_='anId')
    get_authorization()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_authorization = pycamunda.authorization.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_authorization()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.authorization.Authorization', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_authorization = pycamunda.authorization.Get(url=engine_url, id_='anId')
    get_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.resource.ResourceType', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_get_returns_authorizations(engine_url):
    get_authorization = pycamunda.authorization.Get(url=engine_url, id_='anId')
    authorizations = get_authorization()

    assert isinstance(authorizations, pycamunda.authorization.Authorization)
