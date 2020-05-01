# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_externaltask_json():
    return {
        'activityId': 'anActivityId',
        'activityInstanceId': 'anActivityInstanceId',
        'errorMessage': 'anErrorMessage',
        'errorDetails': 'anErrorDetail',
        'executionId': 'anExecutionId',
        'id': 'anId',
        'processDefinitionId': 'aProcessDefinitionId',
        'processDefinitionKey': 'aProcessDefinitionKey',
        'processInstanceId': 'aProcessInstanceId',
        'tenantId': 'aTenantId',
        'retries': 10,
        'workerId': 'aWorkerId',
        'priority': 50,
        'topicName': 'aTopicName',
        'lockExpirationTime': '2000-01-01T01:01:00.000+0000',
        'suspended': True,
        'businessKey': 'aBusinessKey',
        'variables': {'aVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}}}
    }
