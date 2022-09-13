# -*- coding: utf-8 -*-

import pytest

import pycamunda.externaltask
import pycamunda.variable
import pycamunda.base


def test_externaltask_load_definition(my_externaltask_json):
    json_ = dict(my_externaltask_json)
    external_task = pycamunda.externaltask.ExternalTask.load(json_)

    assert external_task.activity_id == json_['activityId']
    assert external_task.activity_instance_id == json_['activityInstanceId']
    assert external_task.error_message == json_['errorMessage']
    assert external_task.error_details == json_['errorDetails']
    assert external_task.execution_id == json_['executionId']
    assert external_task.id_ == json_['id']
    assert external_task.process_definition_id == json_['processDefinitionId']
    assert external_task.process_definition_key == json_['processDefinitionKey']
    assert external_task.process_instance_id == json_['processInstanceId']
    assert external_task.tenant_id == json_['tenantId']
    assert external_task.retries == json_['retries']
    assert external_task.worker_id == json_['workerId']
    assert external_task.priority == json_['priority']
    assert external_task.topic_name == json_['topicName']
    assert external_task.lock_expiration_time == pycamunda.base.from_isoformat(json_['lockExpirationTime'])
    assert external_task.suspended == json_['suspended']
    assert external_task.business_key == json_['businessKey']
    assert external_task.variables == {
                var_name: pycamunda.variable.Variable(
                    type_=var['type'], value=var['value'], value_info=var['valueInfo']
                )
                for var_name, var in json_['variables'].items()
            }


def test_externaltask_load_definition_without_error_details(my_externaltask_json):
    json_ = dict(my_externaltask_json)
    del json_['errorDetails']
    external_task = pycamunda.externaltask.ExternalTask.load(json_)

    assert external_task.error_details is None


def test_externaltask_load_raises_keyerror(my_externaltask_json):
    for key in {
        key: val for key, val in my_externaltask_json.items()
        if key not in {'suspended', 'businessKey', 'variables', 'errorDetails'}
    }:
        json_ = dict(my_externaltask_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.externaltask.ExternalTask.load(data=json_)
