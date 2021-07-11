# -*- coding: utf-8 -*-

import pytest

import pycamunda.migration


def test_migrationinstruction_load_definition(my_instruction_json):

    migration_instruction = pycamunda.migration.MigrationInstruction.load(my_instruction_json)

    assert migration_instruction.source_activity_ids == my_instruction_json['sourceActivityIds']
    assert migration_instruction.target_activity_ids == my_instruction_json['targetActivityIds']
    assert migration_instruction.update_event_trigger == my_instruction_json['updateEventTrigger']


def test_migrationinstruction_load_raises_key_error(my_instruction_json):
    for key in my_instruction_json:
        json_ = dict(my_instruction_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.migration.MigrationInstruction.load(data=json_)
