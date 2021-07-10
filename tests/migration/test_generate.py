# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.migration
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_generate_params(engine_url, generate_input, generate_output):
    generate_migration = pycamunda.migration.Generate(url=engine_url, **generate_input)

    assert generate_migration.url == engine_url + '/migration/generate'
    assert generate_migration.query_parameters() == {}
    assert generate_migration.body_parameters() == generate_output


@unittest.mock.patch('pycamunda.migration.MigrationPlan', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_generate_calls_requests(mock, engine_url, generate_input):
    generate_migration = pycamunda.migration.Generate(url=engine_url, **generate_input)
    generate_migration()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_generate_raises_pycamunda_exception(engine_url, generate_input):
    generate_migration = pycamunda.migration.Generate(url=engine_url, **generate_input)
    with pytest.raises(pycamunda.PyCamundaException):
        generate_migration()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.migration.MigrationPlan', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_generate_raises_for_status(mock, engine_url, generate_input):
    generate_migration = pycamunda.migration.Generate(url=engine_url, **generate_input)
    generate_migration()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_generate_returns_migrationplan(engine_url, generate_input):
    generate_migration = pycamunda.migration.Generate(url=engine_url, **generate_input)
    migration_plan = generate_migration()

    assert isinstance(migration_plan, pycamunda.migration.MigrationPlan)
