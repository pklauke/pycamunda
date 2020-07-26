# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.identity
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getgroups_params(engine_url):
    get_users_groups = pycamunda.identity.GetGroups(url=engine_url, user_id='anId')

    assert get_users_groups.url == engine_url + '/identity/groups'
    assert get_users_groups.query_parameters() == {'userId': 'anId'}
    assert get_users_groups.body_parameters() == {}


@unittest.mock.patch('pycamunda.identity.UsersGroups.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_getgroups_calls_requests(mock, engine_url):
    get_users_groups = pycamunda.identity.GetGroups(url=engine_url, user_id='anId')
    get_users_groups()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getgroups_raises_pycamunda_exception(engine_url):
    get_users_groups = pycamunda.identity.GetGroups(url=engine_url, user_id='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_users_groups()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.identity.UsersGroups', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getgroups_raises_for_status(mock, engine_url):
    get_users_groups = pycamunda.identity.GetGroups(url=engine_url, user_id='anId')
    get_users_groups()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getgroups_returns_usersgroups(engine_url):
    get_users_groups = pycamunda.identity.GetGroups(url=engine_url, user_id='anId')
    users_groups = get_users_groups()

    assert isinstance(users_groups, pycamunda.identity.UsersGroups)
