# -*- coding: utf-8 -*-

import pytest

import pycamunda.processinst


def test_processinstance_load(my_process_instance_json):
    process_instance = pycamunda.processinst.ProcessInstance.load(my_process_instance_json)

    assert process_instance.id_ == my_process_instance_json['id']
    assert process_instance.definition_id == my_process_instance_json['definitionId']
    assert process_instance.business_key == my_process_instance_json['businessKey']
    assert process_instance.case_instance_id == my_process_instance_json['caseInstanceId']
    assert process_instance.suspended == my_process_instance_json['suspended']
    assert process_instance.tenant_id == my_process_instance_json['tenantId']
    assert process_instance.links == tuple()


def test_processinstance_load_raises_keyerror(my_process_instance_json):
    for key in my_process_instance_json:
        json = dict(my_process_instance_json)
        del json[key]
        with pytest.raises(KeyError):
            pycamunda.processinst.ProcessInstance.load(data=json)
