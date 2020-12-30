# -*- coding: utf-8 -*-

import datetime as dt

import pytest

import pycamunda.base


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


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'topic_name': 'aTopicName',
        'worker_id': 'aWorkerId',
        'locked': True,
        'not_locked': True,
        'with_retries_left': True,
        'no_retries_left': True,
        'lock_expiration_after': dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1),
        'lock_expiration_before': dt.datetime(
            year=2020, month=1, day=1, hour=1, minute=1, second=1
        ),
        'activity_id': 'anActivityId',
        'activity_id_in': [],
        'execution_id': 'anExecutionId',
        'process_instance_id': 'aProcessInstanceId',
        'process_definition_id': 'aProcessDefinitionId',
        'tenant_id_in': [],
        'active': True,
        'priority_higher_equals': 10,
        'priority_lower_equals': 20,
        'suspended': True,
        'sort_by': 'id_',
        'ascending': True,
        'first_result': 1,
        'max_results': 100
    }


@pytest.fixture
def getlist_output():
    return {
        'externalTaskId': 'anId',
        'topicName': 'aTopicName',
        'workerId': 'aWorkerId',
        'locked': 'true',
        'notLocked': 'true',
        'withRetriesLeft': 'true',
        'noRetriesLeft': 'true',
        'lockExpirationAfter': pycamunda.base.isoformat(
            dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
        ),
        'lockExpirationBefore': pycamunda.base.isoformat(
            dt.datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
        ),
        'activityId': 'anActivityId',
        'activityIdIn': [],
        'executionId': 'anExecutionId',
        'processInstanceId': 'aProcessInstanceId',
        'processDefinitionId': 'aProcessDefinitionId',
        'tenantIdIn': [],
        'active': 'true',
        'priorityHigherThanOrEquals': 10,
        'priorityLowerThanOrEquals': 20,
        'suspended': 'true',
        'sortBy': 'id',
        'sortOrder': 'asc',
        'firstResult': 1,
        'maxResults': 100
    }
