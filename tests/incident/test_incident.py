# -*- coding: utf-8 -*-

import datetime as dt

import pytest

import pycamunda.incident


def test_incident_load(my_incident_json):
    incident = pycamunda.incident.Incident.load(my_incident_json)

    assert incident.id_ == my_incident_json['id']
    assert incident.process_definition_id == my_incident_json['processDefinitionId']
    assert incident.process_instance_id == my_incident_json['processInstanceId']
    assert incident.execution_id == my_incident_json['executionId']
    assert incident.incident_type == pycamunda.incident.IncidentType(
        my_incident_json['incidentType']
    )
    assert incident.activity_id == my_incident_json['activityId']
    assert incident.cause_incident_id == my_incident_json['causeIncidentId']
    assert incident.root_cause_incident_id == my_incident_json['rootCauseIncidentId']
    assert incident.configuration == my_incident_json['configuration']
    assert incident.tenant_id == my_incident_json['tenantId']
    assert incident.incident_message == my_incident_json['incidentMessage']
    assert incident.job_definition_id == my_incident_json['jobDefinitionId']
    assert incident.incident_timestamp == dt.datetime(
        year=2000, month=1, day=1, hour=0, minute=0, second=0, tzinfo=dt.timezone.utc
    )


def test_incident_load_raises_keyerror(my_incident_json):
    for key in (k for k in my_incident_json if k != 'incidentTimestamp'):
        json_ = dict(my_incident_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.incident.Incident.load(json_)
