# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')

    assert create_user.url == engine_url + '/user/create'
    assert create_user.query_parameters() == {}
    assert create_user.body_parameters() == {
        'profile': {
            'id': 'janedoe',
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'jane.doe@email.com'
        },
        'credentials': {
            'password': 'password'
        }
    }


@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    create_user()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    with pytest.raises(pycamunda.PyCamundaException):
        create_user()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    create_user()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_returns_none(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    result = create_user()

    assert result is None
