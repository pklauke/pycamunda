# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.migration
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_validate_params(engine_url, generate_input, generate_output):
    validate_migration = pycamunda.migration.Validate(
        url=engine_url,
        source_process_definition_id='anId',
        target_process_definition_id='anotherId'
    )
    validate_migration.add_instruction(
        source_activity_ids=['anId'],
        target_activity_ids=['anotherId'],
        update_event_trigger=True
    )

    assert validate_migration.url == engine_url + '/migration/validate'
    assert validate_migration.query_parameters() == {}
    assert validate_migration.body_parameters() == {
        'sourceProcessDefinitionId': 'anId',
        'targetProcessDefinitionId': 'anotherId',
        'instructions': [{
            'sourceActivityIds': ['anId'],
            'targetActivityIds': ['anotherId'],
            'updateEventTrigger': True
        }]
    }


def test_validate_from_migration_plan_params(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    validate_migration = pycamunda.migration.Validate.from_migration_plan(
        url=engine_url, migration_plan=migration_plan
    )

    assert validate_migration.body_parameters() == my_plan_json


@unittest.mock.patch('pycamunda.migration.InstructionReport', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_validate_calls_requests(mock, engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    validate_migration = pycamunda.migration.Validate.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan
    )
    validate_migration()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_validate_raises_pycamunda_exception(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    validate_migration = pycamunda.migration.Validate.from_migration_plan(
        url=engine_url, migration_plan=migration_plan
    )
    with pytest.raises(pycamunda.PyCamundaException):
        validate_migration()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.migration.InstructionReport', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_validate_raises_for_status(mock, engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    validate_migration = pycamunda.migration.Validate.from_migration_plan(
        url=engine_url, migration_plan=migration_plan
    )
    validate_migration()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_validate_returns_migrationplan(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    validate_migration = pycamunda.migration.Validate.from_migration_plan(
        url=engine_url, migration_plan=migration_plan
    )
    instruction_reports = validate_migration()

    assert isinstance(instruction_reports, tuple)
    assert all(
        isinstance(report, pycamunda.migration.InstructionReport) for report in instruction_reports
    )
