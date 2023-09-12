# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_definitions = pycamunda.processdef.GetList(url=engine_url, **getlist_input)

    assert get_definitions.url == engine_url + '/process-definition'
    assert get_definitions.query_parameters() == getlist_output
    assert get_definitions.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests_with_timeout(mock, engine_url):
    get_definitions = pycamunda.processdef.GetList(url=engine_url, id_='anId', timeout=23)
    get_definitions()
    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'
    assert mock.call_args[1]['timeout'] == 23

@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_definitions = pycamunda.processdef.GetList(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_definitions()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ProcessDefinition', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_definitions = pycamunda.processdef.GetList(url=engine_url, id_='anId')
    get_definitions()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getlist_returns_response_content(engine_url):
    get_definitions = pycamunda.processdef.GetList(url=engine_url, id_='anId')
    definitions = get_definitions()

    assert isinstance(definitions, tuple)
