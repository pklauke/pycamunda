# -*- coding: utf-8 -*-

import pytest

import pycamunda.caseinst


def test_caseinstance_load(my_case_instance_json):
    case_instance = pycamunda.caseinst.CaseInstance.load(my_case_instance_json)

    assert case_instance.id_ == my_case_instance_json['id']
    assert case_instance.definition_id == my_case_instance_json['caseDefinitionId']
    assert case_instance.tenant_id == my_case_instance_json['tenantId']
    assert case_instance.business_key == my_case_instance_json['businessKey']
    assert case_instance.active == my_case_instance_json['active']


def test_caseinstance_load_raises_keyerror(my_case_instance_json):
    for key in my_case_instance_json:
        json_ = dict(my_case_instance_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.caseinst.CaseInstance.load(data=json_)
