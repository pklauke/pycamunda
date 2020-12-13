# -*- coding: utf-8 -*-

import pytest

import pycamunda.casedef


def test_case_definition_load(my_case_definition_json):
    case_definition = pycamunda.casedef.CaseDefinition.load(my_case_definition_json)

    assert case_definition.id_ == my_case_definition_json['id']
    assert case_definition.key == my_case_definition_json['key']
    assert case_definition.category == my_case_definition_json['category']
    assert case_definition.name == my_case_definition_json['name']
    assert case_definition.version == my_case_definition_json['version']
    assert case_definition.resource == my_case_definition_json['resource']
    assert case_definition.deployment_id == my_case_definition_json['deploymentId']
    assert case_definition.tenant_id == my_case_definition_json['tenantId']
    assert case_definition.history_time_to_live == my_case_definition_json['historyTimeToLive']


def test_case_definition_load_raises_keyerror(my_case_definition_json):
    for key in my_case_definition_json:
        json_ = dict(my_case_definition_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.casedef.CaseDefinition.load(data=json_)
