# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_incidents = pycamunda.incident.GetList(url=engine_url, **getlist_input)

    assert get_incidents.url == engine_url + '/incident'
    assert get_incidents.query_parameters() == getlist_output
    assert get_incidents.body_parameters() == {}


@unittest.mock.patch('pycamunda.incident.Incident.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.get')
def test_getlist_calls_requests(mock, engine_url):
    get_incidents = pycamunda.incident.GetList(url=engine_url)
    get_incidents()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_incidents = pycamunda.incident.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_incidents()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.incident.Incident', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_incidents = pycamunda.incident.GetList(url=engine_url)
    get_incidents()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.incident.IncidentType', unittest.mock.MagicMock())
def test_getlist_returns_incidents_tuple(engine_url):
    get_incidents = pycamunda.incident.GetList(url=engine_url)
    incidents = get_incidents()

    assert isinstance(incidents, tuple)
    assert all(isinstance(incident, pycamunda.incident.IncidentType) for incident in incidents)
