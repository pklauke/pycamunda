# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.activityinst
import pycamunda.incident


INCIDENT_TYPE_COUNT = pycamunda.incident.IncidentTypeCount(
    incident_type=pycamunda.incident.IncidentType.failed_job,
    incident_count=1
)


@unittest.mock.patch(
    'pycamunda.incident.IncidentTypeCount.load',
    lambda _: INCIDENT_TYPE_COUNT
)
def test_transition_instance_load(my_transition_instance_json):
    instance = pycamunda.activityinst.TransitionInstance.load(my_transition_instance_json)

    assert instance.id_ == my_transition_instance_json['id']
    assert instance.activity_id == my_transition_instance_json['activityId']
    assert instance.activity_name == my_transition_instance_json['activityName']
    assert instance.activity_type == my_transition_instance_json['activityType']
    assert instance.process_instance_id == my_transition_instance_json['processInstanceId']
    assert instance.process_definition_id == my_transition_instance_json['processDefinitionId']
    assert instance.execution_ids == tuple(my_transition_instance_json['executionId'])
    assert instance.incident_ids == tuple(my_transition_instance_json['incidentIds'])
    assert instance.incidents == (INCIDENT_TYPE_COUNT, )


def test_transition_instance_load_raises_keyerror(my_transition_instance_json):
    for key in my_transition_instance_json:
        json_ = dict(my_transition_instance_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.activityinst.TransitionInstance.load(json_)
