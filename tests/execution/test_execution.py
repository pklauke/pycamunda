# -*- coding: utf-8 -*-

import pytest

import pycamunda.execution


def test_execution_load(my_execution_json):
    execution = pycamunda.execution.Execution.load(my_execution_json)

    assert execution.id_ == my_execution_json['id']
    assert execution.process_instance_id == my_execution_json['processInstanceId']
    assert execution.ended == my_execution_json['ended']
    assert execution.tenant_id == my_execution_json['tenantId']


def test_execution_load_raises_keyerror(my_execution_json):
    for key in my_execution_json:
        json_ = dict(my_execution_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.execution.Execution.load(json_)
