# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_create_params(engine_url):
    create_group = pycamunda.group.Create(url=engine_url, id_='anId', name='aName', type_='aType')

    assert create_group.url == engine_url + '/group/create'
    assert create_group.query_parameters() == {}
    assert create_group.body_parameters() == {
        'id': 'anId', 'name': 'aName', 'type': 'aType'
    }


@unittest.mock.patch('requests.Session.request')
def test_create_calls_requests(mock, engine_url):
    create_group = pycamunda.group.Create(url=engine_url, id_='anId', name='aName', type_='aType')
    create_group()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url):
    create_group = pycamunda.group.Create(url=engine_url, id_='anId', name='aName', type_='aType')
    with pytest.raises(pycamunda.PyCamundaException):
        create_group()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url):
    create_group = pycamunda.group.Create(url=engine_url, id_='anId', name='aName', type_='aType')
    create_group()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_create_returns_none(engine_url):
    create_group = pycamunda.group.Create(url=engine_url, id_='anId', name='aName', type_='aType')
    result = create_group()

    assert result is None
