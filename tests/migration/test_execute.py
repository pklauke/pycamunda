# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.migration
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_execute_params(engine_url, my_plan_json):
    execute_migration = pycamunda.migration.Execute(
        url=engine_url,
        source_process_definition_id='anId',
        target_process_definition_id='anotherId',
        process_instance_ids=['yetAnotherId'],
        skip_custom_listeners=True,
        skip_io_mappings=True
    )
    execute_migration.add_instruction(
        source_activity_ids=['anActivityId'],
        target_activity_ids=['anotherActivityId'],
        update_event_trigger=True
    )

    assert execute_migration.url == engine_url + '/migration/execute'
    assert execute_migration.query_parameters() == {}
    assert execute_migration.body_parameters() == {
        'processInstanceIds': ['yetAnotherId'],
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'migrationPlan': {
            'sourceProcessDefinitionId': 'anId',
            'targetProcessDefinitionId': 'anotherId',
            'instructions': [{
                'sourceActivityIds': ['anActivityId'],
                'targetActivityIds': ['anotherActivityId'],
                'updateEventTrigger': True
            }]
        }
    }


def test_execute_from_migration_plan_params(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True
    )

    assert execute_migration.url == engine_url + '/migration/execute'
    assert execute_migration.query_parameters() == {}
    assert execute_migration.body_parameters() == {
        'processInstanceIds': ['anId'],
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'migrationPlan': {
            'sourceProcessDefinitionId': 'anId',
            'targetProcessDefinitionId': 'anotherId',
            'instructions': [{
                'sourceActivityIds': ['anId'],
                'targetActivityIds': ['anotherId'],
                'updateEventTrigger': False
            }, {
                'sourceActivityIds': ['anId'],
                'targetActivityIds': ['anotherId'],
                'updateEventTrigger': False
            }
            ]
        }
    }


def test_execute_async_params(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True,
        async_=True
    )

    assert execute_migration.url == engine_url + '/migration/executeAsync'


@unittest.mock.patch('requests.Session.request')
def test_execute_calls_requests(mock, engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True,
        async_=True
    )
    execute_migration()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_execute_raises_pycamunda_exception(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True,
        async_=True
    )
    with pytest.raises(pycamunda.PyCamundaException):
        execute_migration()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_execute_raises_for_status(mock, engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True,
        async_=True
    )
    execute_migration()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_execute_returns_none(engine_url, my_plan_json):
    migration_plan = pycamunda.migration.MigrationPlan.load(data=my_plan_json)
    execute_migration = pycamunda.migration.Execute.from_migration_plan(
        url=engine_url,
        migration_plan=migration_plan,
        process_instance_ids=['anId'],
        skip_custom_listeners=True,
        skip_io_mappings=True,
        async_=True
    )
    result = execute_migration()

    assert result is None
