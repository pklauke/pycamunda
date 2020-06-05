# -*- coding: utf-8 -*-

import pytest

import pycamunda.variable


def test_variableinstance_load(my_variableinstance_json):
    variable_instance = pycamunda.variable.VariableInstance.load(my_variableinstance_json)

    assert variable_instance.id_ == my_variableinstance_json['id']
    assert variable_instance.name == my_variableinstance_json['name']
    assert variable_instance.type_ == my_variableinstance_json['type']
    assert variable_instance.value == my_variableinstance_json['value']
    assert variable_instance.value_info == my_variableinstance_json['valueInfo']
    assert variable_instance.process_instance_id == my_variableinstance_json['processInstanceId']
    assert variable_instance.execution_id == my_variableinstance_json['executionId']
    assert variable_instance.case_instance_id == my_variableinstance_json['caseInstanceId']
    assert variable_instance.case_execution_id == my_variableinstance_json['caseExecutionId']
    assert variable_instance.task_id == my_variableinstance_json['taskId']
    assert variable_instance.activity_instance_id == my_variableinstance_json['activityInstanceId']
    assert variable_instance.tenant_id == my_variableinstance_json['tenantId']
    assert variable_instance.error_message == my_variableinstance_json['errorMessage']


def test_variableinstance_load_raises_keyerror(my_variableinstance_json):
    for key in my_variableinstance_json:
        json_ = dict(my_variableinstance_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.variable.VariableInstance.load(data=json_)
