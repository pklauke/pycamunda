# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_group = pycamunda.group.Get(url=engine_url, id_='anId')

    assert get_group.url == engine_url + '/group/anId'
    assert get_group.query_parameters() == {}
    assert get_group.body_parameters() == {}


@unittest.mock.patch('pycamunda.group.Group.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_group = pycamunda.group.Get(url=engine_url, id_='anId')
    get_group()

    assert mock.called
    assert mock.call_args[1]['method'] == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_group = pycamunda.group.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_group()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.group.Group', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_group = pycamunda.group.Get(url=engine_url, id_='anId')
    get_group()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_get_returns_group(engine_url):
    get_group = pycamunda.group.Get(url=engine_url, id_='anId')
    group = get_group()

    assert isinstance(group, pycamunda.group.Group)
