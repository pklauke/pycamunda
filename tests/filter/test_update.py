# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url):
    update_filter = pycamunda.filter.Update(
        url=engine_url, id_='anId', name='aName', owner='anOwner'
    )

    assert update_filter.url == engine_url + '/filter/anId'
    assert update_filter.query_parameters() == {}
    assert update_filter.body_parameters() == {
        'name': 'aName', 'owner': 'anOwner', 'query': {}, 'resourceType': 'Task'
    }


@unittest.mock.patch('requests.Session.request')
def test_update_calls_requests(mock, engine_url):
    update_filter = pycamunda.filter.Update(
        url=engine_url, id_='anId', name='aName', owner='anOwner'
    )
    update_filter()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url):
    update_filter = pycamunda.filter.Update(
        url=engine_url, id_='anId', name='aName', owner='anOwner'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_filter()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.filter.Filter')
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url):
    update_filter = pycamunda.filter.Update(
        url=engine_url, id_='anId', name='aName', owner='anOwner'
    )
    update_filter()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_update_returns_none(engine_url):
    update_filter = pycamunda.filter.Update(
        url=engine_url, id_='anId', name='aName', owner='anOwner'
    )
    result = update_filter()

    assert result is None
