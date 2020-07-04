# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_resolve_params(engine_url):
    resolve_incident = pycamunda.incident.Resolve(url=engine_url, id_='anId')

    assert resolve_incident.url == engine_url + '/incident/anId'
    assert resolve_incident.query_parameters() == {}
    assert resolve_incident.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_resolve_calls_requests(mock, engine_url):
    resolve_incident = pycamunda.incident.Resolve(url=engine_url, id_='anId')
    resolve_incident()

    assert mock.called
    assert mock.call_args[1]['method'] == 'DELETE'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_resolve_raises_pycamunda_exception(engine_url):
    resolve_incident = pycamunda.incident.Resolve(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        resolve_incident()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_resolve_raises_for_status(mock, engine_url):
    resolve_incident = pycamunda.incident.Resolve(url=engine_url, id_='anId')
    resolve_incident()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_resolve_returns_none(engine_url):
    resolve_incident = pycamunda.incident.Resolve(url=engine_url, id_='anId')
    result = resolve_incident()

    assert result is None
