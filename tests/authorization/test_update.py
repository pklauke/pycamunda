# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.authorization
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url, update_input, update_output):
    update_authorization = pycamunda.authorization.Update(url=engine_url, **update_input)

    assert update_authorization.url == engine_url + '/authorization/anId'
    assert update_authorization.query_parameters() == {}
    assert update_authorization.body_parameters() == update_output


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_update_raises_assert(engine_url, update_input):
    update_authorization = pycamunda.authorization.Update(
        url=engine_url, **update_input, group_id='*'
    )

    with pytest.raises(AssertionError):
        update_authorization()


@unittest.mock.patch('requests.Session.request')
def test_update_calls_requests(mock, engine_url, update_input):
    update_authorization = pycamunda.authorization.Update(url=engine_url, **update_input)
    update_authorization()

    assert mock.called
    assert mock.call_args[1]['method'] == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url, update_input):
    update_authorization = pycamunda.authorization.Update(url=engine_url, **update_input)
    with pytest.raises(pycamunda.PyCamundaException):
        update_authorization()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url, update_input):
    update_authorization = pycamunda.authorization.Update(url=engine_url, **update_input)
    update_authorization()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_update_returns_none(engine_url, update_input):
    update_authorization = pycamunda.authorization.Update(url=engine_url, **update_input)
    result = update_authorization()

    assert result is None
