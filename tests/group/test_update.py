# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url):
    update_group = pycamunda.group.Update(url=engine_url, id_='anId', name='aName', type_='aType')

    assert update_group.url == engine_url + '/group/anId'
    assert update_group.query_parameters() == {}
    assert update_group.body_parameters() == {'name': 'aName', 'type': 'aType', 'id': 'anId'}


@unittest.mock.patch('requests.Session.request')
def test_update_calls_requests(mock, engine_url):
    update_group = pycamunda.group.Update(url=engine_url, id_='anId', name='aName', type_='aType')
    update_group()

    assert mock.called
    assert mock.call_args[1]['method'] == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url):
    update_group = pycamunda.group.Update(url=engine_url, id_='anId', name='aName', type_='aType')
    with pytest.raises(pycamunda.PyCamundaException):
        update_group()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url):
    update_group = pycamunda.group.Update(url=engine_url, id_='anId', name='aName', type_='aType')
    update_group()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_update_returns_none(engine_url):
    update_group = pycamunda.group.Update(url=engine_url, id_='anId', name='aName', type_='aType')
    result = update_group()

    assert result is None
