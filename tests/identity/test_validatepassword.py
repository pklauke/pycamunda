# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.identity
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_validatepassword_params(engine_url):
    validate_password = pycamunda.identity.ValidatePassword(url=engine_url, password='aPass')

    assert validate_password.url == engine_url + '/identity/password-policy'
    assert validate_password.query_parameters() == {}
    assert validate_password.body_parameters() == {'password': 'aPass'}


@unittest.mock.patch('pycamunda.identity.PasswordPolicyCompliance.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_validatepassword_calls_requests(mock, engine_url):
    validate_password = pycamunda.identity.ValidatePassword(url=engine_url, password='aPass')
    validate_password()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_validatepassword_raises_pycamunda_exception(engine_url):
    validate_password = pycamunda.identity.ValidatePassword(url=engine_url, password='aPass')
    with pytest.raises(pycamunda.PyCamundaException):
        validate_password()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.identity.PasswordPolicy', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_validatepassword_raises_for_status(mock, engine_url):
    validate_password = pycamunda.identity.ValidatePassword(url=engine_url, password='aPass')
    with pytest.raises(KeyError):
        validate_password()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_validatepassword_returns_tuple(engine_url):
    validate_password = pycamunda.identity.ValidatePassword(url=engine_url, password='aPass')
    password_compliance = validate_password()

    assert isinstance(password_compliance, tuple)
