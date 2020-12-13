# -*- coding: utf-8 -*-

import pytest

import pycamunda.deployment
import pycamunda.base


def test_deployment_with_definitions_load(my_depl_with_def_json):
    depl_with_def = pycamunda.deployment.DeploymentWithDefinitions.load(
        my_depl_with_def_json
    )

    assert depl_with_def.links == my_depl_with_def_json['links']
    assert depl_with_def.id_ == my_depl_with_def_json['id']
    assert depl_with_def.name == my_depl_with_def_json['name']
    assert depl_with_def.source == my_depl_with_def_json['source']
    assert depl_with_def.deployed_process_definitions == my_depl_with_def_json[
        'deployedProcessDefinitions'
    ]
    assert depl_with_def.deployed_case_definitions == my_depl_with_def_json[
        'deployedCaseDefinitions'
    ]
    assert depl_with_def.deployed_decision_definitions == my_depl_with_def_json[
        'deployedDecisionDefinitions'
    ]
    assert depl_with_def.deployed_decision_requirements_definitions == my_depl_with_def_json[
        'deployedDecisionRequirementsDefinitions'
    ]
    assert depl_with_def.tenant_id == my_depl_with_def_json['tenantId']
    assert depl_with_def.deployment_time == pycamunda.base.from_isoformat(
        my_depl_with_def_json['deploymentTime']
    )


def test_deployment_with_definitions_load_raises_keyerror(my_depl_with_def_json):
    for key in my_depl_with_def_json:
        json_ = dict(my_depl_with_def_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.deployment.DeploymentWithDefinitions.load(data=json_)
