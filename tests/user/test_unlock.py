# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_unlock_user_params(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')

    assert unlock_user.url == engine_url + '/user/myuserid/unlock'
    assert unlock_user.query_parameters() == {}
    assert unlock_user.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_unlock_calls_requests(mock, engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    unlock_user()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_unlock_raises_pycamunda_exception(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')

    with pytest.raises(pycamunda.PyCamundaException):
        unlock_user()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_unlock_raises_for_status(mock, engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    unlock_user()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_unlock_returns_none(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    result = unlock_user()

    assert result is None
