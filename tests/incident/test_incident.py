# -*- coding: utf-8 -*-

import pytest

import pycamunda.incident


def test_incident_load():
    incident = pycamunda.incident.IncidentTypeCount.load(
        {'incidentType': 'failedJob', 'incidentCount': 10}
    )

    assert incident.incident_type == pycamunda.incident.IncidentType.failed_job
    assert incident.incident_count == 10


def test_incident_load_raises_keyerror():
    incident_json = {'incidentType': 'failedJob', 'incidentCount': 10}
    for key in incident_json:
        json_ = dict(incident_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.incident.IncidentTypeCount.load(json_)
