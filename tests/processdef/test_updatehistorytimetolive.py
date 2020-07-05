# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
import pycamunda.incident
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, response_mock


def test_updatehistorytimetolive_params(engine_url):
    update_definition = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )

    assert update_definition.url == engine_url + '/process-definition/anId/history-time-to-live'
    assert update_definition.query_parameters() == {}
    assert update_definition.body_parameters() == {'historyTimeToLive': 10}


def test_updatehistorytimetolive_path(engine_url):
    update_definition_id = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )
    update_definition_key = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, key='aKey', history_time_to_live=10
    )
    update_definition_tenant = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, key='aKey', tenant_id='aTenantId', history_time_to_live=10
    )

    assert update_definition_id.url == engine_url + '/process-definition/anId/history-time-to-live'
    assert update_definition_key.url == engine_url + '/process-definition/key/aKey' \
                                                     '/history-time-to-live'
    assert update_definition_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                        '/tenant-id/aTenantId/history-time-to-live'


@unittest.mock.patch('requests.Session.request')
def test_updatehistorytimetolive_calls_requests(mock, engine_url):
    update_definition = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )
    update_definition()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_updatehistorytimetolive_raises_pycamunda_exception(engine_url):
    update_definition = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_definition()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_updatehistorytimetolive_raises_for_status(mock, engine_url):
    update_definition = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )
    update_definition()

    assert mock.called


@unittest.mock.patch('requests.Session.request', response_mock)
def test_updatehistorytimetolive_returns_none(engine_url):
    update_definition = pycamunda.processdef.UpdateHistoryTimeToLive(
        url=engine_url, id_='anId', history_time_to_live=10
    )
    result = update_definition()

    assert result is None
