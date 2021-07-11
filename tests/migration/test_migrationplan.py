# -*- coding: utf-8 -*-

import pytest

import pycamunda.migration


def test_migrationplan_load_definition(my_plan_json):

    migration_plan = pycamunda.migration.MigrationPlan.load(my_plan_json)

    assert migration_plan.source_process_definition_id == my_plan_json['sourceProcessDefinitionId']
    assert migration_plan.target_process_definition_id == my_plan_json['targetProcessDefinitionId']
    assert migration_plan.instructions == tuple(
        pycamunda.migration.MigrationInstruction.load(plan_json)
        for plan_json in my_plan_json['instructions']
    )


def test_migrationplan_load_raises_key_error(my_plan_json):
    for key in my_plan_json:
        json_ = dict(my_plan_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.migration.MigrationPlan.load(data=json_)
