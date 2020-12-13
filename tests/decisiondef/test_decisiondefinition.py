# -*- coding: utf-8 -*-

import pytest

import pycamunda.decisiondef


def test_decision_definition_load(my_decision_definition_json):
    decision_definition = pycamunda.decisiondef.DecisionDefinition.load(my_decision_definition_json)

    assert decision_definition.id_ == my_decision_definition_json['id']
    assert decision_definition.key == my_decision_definition_json['key']
    assert decision_definition.category == my_decision_definition_json['category']
    assert decision_definition.name == my_decision_definition_json['name']
    assert decision_definition.version == my_decision_definition_json['version']
    assert decision_definition.resource == my_decision_definition_json['resource']
    assert decision_definition.deployment_id == my_decision_definition_json['deploymentId']
    assert decision_definition.decision_requirements_definition_id == my_decision_definition_json[
        'decisionRequirementsDefinitionId'
    ]
    assert decision_definition.decision_requirements_definition_key == my_decision_definition_json[
        'decisionRequirementsDefinitionKey'
    ]
    assert decision_definition.tenant_id == my_decision_definition_json['tenantId']
    assert decision_definition.version_tag == my_decision_definition_json['versionTag']
    assert decision_definition.history_time_to_live == my_decision_definition_json[
        'historyTimeToLive'
    ]


def test_decision_definition_load_raises_keyerror(my_decision_definition_json):
    for key in my_decision_definition_json:
        json_ = dict(my_decision_definition_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.decisiondef.DecisionDefinition.load(data=json_)
