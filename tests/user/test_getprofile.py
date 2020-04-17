# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getprofile_params(engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')

    assert get_profile.url == engine_url + '/user/myuserid/profile'
    assert get_profile.query_parameters() == {}
    assert get_profile.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_getprofile_calls_requests(mock, engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    get_profile()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getprofile_raises_pycamunda_exception(engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    with pytest.raises(pycamunda.PyCamundaException):
        get_profile()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.user.User', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getprofile_raises_for_status(mock, engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    get_profile()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
def test_getprofile_returns_user(engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    user_profile = get_profile()

    assert isinstance(user_profile, pycamunda.user.User)
