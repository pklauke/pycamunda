# -*- coding: utf-8 -*-

import pytest

import pycamunda.decisionreqdef


def test_decision_requirements_definition_load(my_decision_req_def_json):
    decision_req_def = pycamunda.decisionreqdef.DecisionRequirementsDefinition.load(
        my_decision_req_def_json
    )

    assert decision_req_def.id_ == my_decision_req_def_json['id']
    assert decision_req_def.key == my_decision_req_def_json['key']
    assert decision_req_def.category == my_decision_req_def_json['category']
    assert decision_req_def.name == my_decision_req_def_json['name']
    assert decision_req_def.version == my_decision_req_def_json['version']
    assert decision_req_def.resource == my_decision_req_def_json['resource']
    assert decision_req_def.deployment_id == my_decision_req_def_json['deploymentId']
    assert decision_req_def.tenant_id == my_decision_req_def_json['tenantId']


def test_decision_requirements_definition_load_raises_keyerror(my_decision_req_def_json):
    for key in my_decision_req_def_json:
        json_ = dict(my_decision_req_def_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.decisionreqdef.DecisionRequirementsDefinition.load(data=json_)
