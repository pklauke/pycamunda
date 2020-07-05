# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_getprocessdiagram_params(engine_url):
    get_process_instance_stats = pycamunda.processdef.GetProcessInstanceStats(
        url=engine_url, failed_jobs=True
    )

    assert get_process_instance_stats.url == engine_url + '/process-definition/statistics'
    assert get_process_instance_stats.query_parameters() == {'failedJobs': True}
    assert get_process_instance_stats.body_parameters() == {}


def test_getprocessdiagram_path(engine_url):
    get_process_instance_stats1 = pycamunda.processdef.GetProcessInstanceStats(
        url=engine_url, incidents=True
    )
    get_process_instance_stats2 = pycamunda.processdef.GetProcessInstanceStats(
        url=engine_url, root_incidents=True
    )
    get_process_instance_stats3 = pycamunda.processdef.GetProcessInstanceStats(
        url=engine_url, incidents_for_type=pycamunda.incident.IncidentType.failed_external_task
    )

    assert get_process_instance_stats1.query_parameters() == {
        'failedJobs': False, 'incidents': True
    }
    assert get_process_instance_stats2.query_parameters() == {
        'failedJobs': False, 'rootIncidents': True
    }
    assert get_process_instance_stats3.query_parameters() == {
        'failedJobs': False,
        'incidentsForType': pycamunda.incident.IncidentType.failed_external_task.value
    }


def test_getprocessdiagramm_raises_exception_on_invalid_inputs(engine_url):
    with pytest.raises(pycamunda.PyCamundaException):
        pycamunda.processdef.GetProcessInstanceStats(
            url=engine_url, incidents=True, root_incidents=True
        )
    with pytest.raises(pycamunda.PyCamundaException):
        pycamunda.processdef.GetProcessInstanceStats(
            url=engine_url,
            incidents=True,
            incidents_for_type=pycamunda.incident.IncidentType.failed_external_task
        )
    with pytest.raises(pycamunda.PyCamundaException):
        pycamunda.processdef.GetProcessInstanceStats(
            url=engine_url,
            root_incidents=True,
            incidents_for_type=pycamunda.incident.IncidentType.failed_external_task
        )
    with pytest.raises(pycamunda.PyCamundaException):
        pycamunda.processdef.GetProcessInstanceStats(
            url=engine_url,
            incidents=True,
            root_incidents=True,
            incidents_for_type=pycamunda.incident.IncidentType.failed_external_task
        )


@unittest.mock.patch('requests.Session.request')
def test_getprocessdiagram_calls_requests(mock, engine_url):
    get_process_instance_stats = pycamunda.processdef.GetProcessInstanceStats(url=engine_url)
    get_process_instance_stats()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getprocessdiagram_raises_pycamunda_exception(engine_url):
    get_process_instance_stats = pycamunda.processdef.GetProcessDiagram(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_process_instance_stats()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ActivityStats', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getprocessdiagram_raises_for_status(mock, engine_url):
    get_process_instance_stats = pycamunda.processdef.GetProcessDiagram(url=engine_url)
    get_process_instance_stats()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_getprocessdiagram_returns_response_content(engine_url):
    get_process_instance_stats = pycamunda.processdef.GetProcessDiagram(url=engine_url)
    result = get_process_instance_stats()

    assert result == 'content'
