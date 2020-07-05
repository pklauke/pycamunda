# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url, create_input, create_output):
    create_authorization = pycamunda.authorization.Create(url=engine_url, **create_input)

    assert create_authorization.url == engine_url + '/authorization/create'
    assert create_authorization.query_parameters() == {}
    assert create_authorization.body_parameters() == create_output


@unittest.mock.patch('pycamunda.authorization.Authorization')
@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_raises_assert(engine_url, create_input):
    create_authorization = pycamunda.authorization.Create(
        url=engine_url, **create_input, group_id='*'
    )

    with pytest.raises(AssertionError):
        create_authorization()


@unittest.mock.patch('pycamunda.authorization.Authorization')
@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url, create_input):
    create_authorization = pycamunda.authorization.Create(url=engine_url, **create_input)
    create_authorization()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url, create_input):
    create_authorization = pycamunda.authorization.Create(url=engine_url, **create_input)
    with pytest.raises(pycamunda.PyCamundaException):
        create_authorization()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.authorization.Authorization', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url, create_input):
    create_authorization = pycamunda.authorization.Create(url=engine_url, **create_input)
    create_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.resource.ResourceType', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_create_returns_authorization(engine_url, create_input):
    create_authorization = pycamunda.authorization.Create(url=engine_url, **create_input)
    authorization = create_authorization()

    assert isinstance(authorization, pycamunda.authorization.Authorization)
