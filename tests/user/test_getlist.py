# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, get_list_input, get_list_params):
    get_users = pycamunda.user.GetList(url=engine_url, **get_list_input)

    assert get_users.url == engine_url + '/user'
    assert get_users.body_parameters() == {}
    assert get_users.query_parameters() == get_list_params


@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests(mock, engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    get_users()

    assert mock.called
    assert mock.call_args[1]['method'] == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_users()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.user.User', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    get_users()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getlist_returns_users(engine_url):
    get_users = pycamunda.user.GetList(url=engine_url, id_='myuserid')
    users = get_users()

    assert isinstance(users, tuple)
    assert all(isinstance(user, pycamunda.user.User) for user in users)
