# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.activityinst
import pycamunda.incident


INCIDENT_TYPE_COUNT = pycamunda.incident.IncidentTypeCount(
    incident_type=pycamunda.incident.IncidentType.failed_job,
    incident_count=1
)


TRANSITION_INSTANCE = pycamunda.activityinst.TransitionInstance(
    id_='anId',
    activity_id='anActivityId',
    activity_name='anActivityName',
    activity_type='anActivityType',
    process_instance_id='anInstanceId',
    process_definition_id='aDefinitionId',
    execution_ids=('anExecutionId',),
    incident_ids=('anIncidentId',),
    incidents=tuple()
)


@unittest.mock.patch(
    'pycamunda.incident.IncidentTypeCount.load',
    lambda _: INCIDENT_TYPE_COUNT
)
@unittest.mock.patch(
    'pycamunda.activityinst.TransitionInstance.load', lambda _: TRANSITION_INSTANCE
)
def test_activity_instance_load(my_activity_instance_json):
    my_activity_instance_json['childActivityInstances'] = [dict(my_activity_instance_json)] * 2
    instance = pycamunda.activityinst.ActivityInstance.load(my_activity_instance_json)

    assert instance.id_ == my_activity_instance_json['id']
    assert instance.parent_activity_instance_id == \
        my_activity_instance_json['parentActivityInstanceId']
    assert instance.activity_id == my_activity_instance_json['activityId']
    assert instance.activity_name == my_activity_instance_json['activityName']
    assert instance.activity_type == my_activity_instance_json['activityType']
    assert instance.process_instance_id == my_activity_instance_json['processInstanceId']
    assert instance.process_definition_id == my_activity_instance_json['processDefinitionId']
    assert len(instance.child_activity_instances) == 2
    assert all(isinstance(inst, pycamunda.activityinst.ActivityInstance)
               for inst in instance.child_activity_instances)
    assert instance.child_transition_instances == (TRANSITION_INSTANCE,)
    assert instance.execution_ids == tuple(my_activity_instance_json['executionIds'])
    assert instance.incident_ids == tuple(my_activity_instance_json['incidentIds'])
    assert instance.incidents == (INCIDENT_TYPE_COUNT, )


@unittest.mock.patch(
    'pycamunda.incident.IncidentTypeCount.load',
    lambda _: INCIDENT_TYPE_COUNT
)
@unittest.mock.patch(
    'pycamunda.activityinst.TransitionInstance.load', lambda _: TRANSITION_INSTANCE
)
def test_activity_instance_load_raises_keyerror(my_activity_instance_json):
    optional_keys = {'incidentIds', 'incidents'}
    for key in (k for k in my_activity_instance_json if k not in optional_keys):
        json_ = dict(my_activity_instance_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.activityinst.ActivityInstance.load(json_)
    for key in optional_keys:
        json_ = dict(my_activity_instance_json)
        del json_[key]
        pycamunda.activityinst.ActivityInstance.load(json_)
