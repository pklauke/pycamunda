# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.identity
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getpasswordpolicy_params(engine_url):
    get_policy = pycamunda.identity.GetPasswordPolicy(url=engine_url)

    assert get_policy.url == engine_url + '/identity/password-policy'
    assert get_policy.query_parameters() == {}
    assert get_policy.body_parameters() == {}


@unittest.mock.patch('pycamunda.identity.PasswordPolicy.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_getpasswordpolicy_calls_requests(mock, engine_url):
    get_policy = pycamunda.identity.GetPasswordPolicy(url=engine_url)
    get_policy()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getpasswordpolicy_raises_pycamunda_exception(engine_url):
    get_policy = pycamunda.identity.GetPasswordPolicy(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_policy()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.identity.PasswordPolicy', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getpasswordpolicy_raises_for_status(mock, engine_url):
    get_policy = pycamunda.identity.GetPasswordPolicy(url=engine_url)
    with pytest.raises(KeyError):
        get_policy()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getpasswordpolicy_returns_tuple(engine_url):
    get_policy = pycamunda.identity.GetPasswordPolicy(url=engine_url)
    password_policy = get_policy()

    assert isinstance(password_policy, tuple)
