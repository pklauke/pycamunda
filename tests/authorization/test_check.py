# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_check_params(engine_url, check_input, check_output):
    check_authorization = pycamunda.authorization.Check(url=engine_url, **check_input)

    assert check_authorization.url == engine_url + '/authorization/check'
    assert check_authorization.query_parameters() == check_output
    assert check_authorization.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_check_calls_requests(mock, engine_url, check_input):
    check_authorization = pycamunda.authorization.Check(url=engine_url, **check_input)
    check_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_check_raises_pycamunda_exception(engine_url, check_input):
    check_authorization = pycamunda.authorization.Check(url=engine_url, **check_input)
    with pytest.raises(pycamunda.PyCamundaException):
        check_authorization()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.authorization.Permission', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_check_raises_for_status(mock, engine_url, check_input):
    check_authorization = pycamunda.authorization.Check(url=engine_url, **check_input)
    check_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_check_returns_permission(engine_url, check_input):
    check_authorization = pycamunda.authorization.Check(url=engine_url, **check_input)
    permission = check_authorization()

    assert isinstance(permission, pycamunda.authorization.Permission)
