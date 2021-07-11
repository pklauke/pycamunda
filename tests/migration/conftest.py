# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_instruction_json():
    return {
        'sourceActivityIds': ['anId'],
        'targetActivityIds': ['anotherId'],
        'updateEventTrigger': False
    }


@pytest.fixture
def my_plan_json(my_instruction_json):
    return {
        'sourceProcessDefinitionId': 'anId',
        'targetProcessDefinitionId': 'anotherId',
        'instructions': [my_instruction_json, my_instruction_json]
    }


@pytest.fixture
def my_report_json(my_instruction_json):
    return {
        'instruction': my_instruction_json,
        'failures': ['There are some errors.']
    }


@pytest.fixture
def generate_input():
    return {
        'source_process_definition_id': 'anId',
        'target_process_definition_id': 'anotherId',
        'update_event_triggers': True
    }


@pytest.fixture
def generate_output():
    return {
        'sourceProcessDefinitionId': 'anId',
        'targetProcessDefinitionId': 'anotherId',
        'updateEventTriggers': True
    }
