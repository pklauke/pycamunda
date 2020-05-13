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
