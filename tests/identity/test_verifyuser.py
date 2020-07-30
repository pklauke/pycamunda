# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.identity
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_verifyuser_params(engine_url):
    verify_user = pycamunda.identity.VerifyUser(url=engine_url, username='anUser', password='aPass')

    assert verify_user.url == engine_url + '/identity/verify'
    assert verify_user.query_parameters() == {}
    assert verify_user.body_parameters() == {'username': 'anUser', 'password': 'aPass'}


@unittest.mock.patch('pycamunda.identity.AuthStatus.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_verifyuser_calls_requests(mock, engine_url):
    verify_user = pycamunda.identity.VerifyUser(url=engine_url, username='anUser', password='aPass')
    verify_user()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_verifyuser_raises_pycamunda_exception(engine_url):
    verify_user = pycamunda.identity.VerifyUser(url=engine_url, username='anUser', password='aPass')
    with pytest.raises(pycamunda.PyCamundaException):
        verify_user()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.identity.AuthStatus', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_verifyuser_raises_for_status(mock, engine_url):
    verify_user = pycamunda.identity.VerifyUser(url=engine_url, username='anUser', password='aPass')
    verify_user()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_verifyuser_returns_authstatus(engine_url):
    verify_user = pycamunda.identity.VerifyUser(url=engine_url, username='anUser', password='aPass')
    auth_status = verify_user()

    assert isinstance(auth_status, pycamunda.identity.AuthStatus)
