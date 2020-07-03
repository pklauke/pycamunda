# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_get_params(engine_url):
    get_incident = pycamunda.incident.Get(url=engine_url, id_='anId')

    assert get_incident.url == engine_url + '/incident/anId'
    assert get_incident.query_parameters() == {}
    assert get_incident.body_parameters() == {}


@unittest.mock.patch('pycamunda.incident.Incident.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_get_calls_requests(mock, engine_url):
    get_incident = pycamunda.incident.Get(url=engine_url, id_='anId')
    get_incident()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_get_raises_pycamunda_exception(engine_url):
    get_incident = pycamunda.incident.Get(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_incident()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.incident.Incident', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_get_raises_for_status(mock, engine_url):
    get_incident = pycamunda.incident.Get(url=engine_url, id_='anId')
    get_incident()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.incident.IncidentType', unittest.mock.MagicMock())
def test_get_returns_incident(engine_url):
    get_incident = pycamunda.incident.Get(url=engine_url, id_='anId')
    incident = get_incident()

    assert isinstance(incident, pycamunda.incident.Incident)
