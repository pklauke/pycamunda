# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_transition_instance_json():
    return {
        'id': 'anId',
        'activityId': 'anActivityId',
        'activityName': 'anActivityName',
        'activityType': 'anActivityType',
        'processInstanceId': 'anInstanceId',
        'processDefinitionId': 'aDefinitionId',
        'executionId': ['anExecutionId'],
        'incidentIds': ['anIncidentId'],
        'incidents': [{}]
    }


@pytest.fixture
def my_activity_instance_json():
    return {
        'id': 'anId',
        'parentActivityInstanceId': 'anActivitInstanceId',
        'activityId': 'anActivityId',
        'activityName': 'anActivityname',
        'activityType': 'anActivityType',
        'processInstanceId': 'anInstanceId',
        'processDefinitionId': 'aDefinitionId',
        'childActivityInstances': [],
        'childTransitionInstances': [{}],
        'executionIds': ['anExecutionId'],
        'name': 'aName',
        'incidentIds': ['anIncidentId'],
        'incidents': [{}]
    }
