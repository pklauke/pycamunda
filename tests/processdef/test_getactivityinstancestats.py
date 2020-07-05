# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processdef
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getactivityinstancestats_params(engine_url):
    get_instance_stats = pycamunda.processdef.GetActivityInstanceStats(
        url=engine_url, id_='anId', failed_jobs=True, incidents=True
    )

    assert get_instance_stats.url == engine_url + '/process-definition/anId/statistics'
    assert get_instance_stats.query_parameters() == {'failedJobs': True, 'incidents': True}
    assert get_instance_stats.body_parameters() == {}


def test_getactivityinstancestats_path(engine_url):
    get_instance_stats_id = pycamunda.processdef.GetActivityInstanceStats(
        url=engine_url, id_='anId'
    )
    get_instance_stats_key = pycamunda.processdef.GetActivityInstanceStats(
        url=engine_url, key='aKey'
    )
    get_instance_stats_tenant = pycamunda.processdef.GetActivityInstanceStats(
        url=engine_url, key='aKey', tenant_id='aTenantId'
    )

    assert get_instance_stats_id.url == engine_url + '/process-definition/anId/statistics'
    assert get_instance_stats_key.url == engine_url + '/process-definition/key/aKey/statistics'
    assert get_instance_stats_tenant.url == engine_url + '/process-definition/key/aKey' \
                                                         '/tenant-id/aTenantId/statistics'


@unittest.mock.patch('requests.Session.request')
def test_getactivityinstancestats_calls_requests(mock, engine_url):
    get_instance_stats = pycamunda.processdef.GetActivityInstanceStats(url=engine_url, id_='anId')
    get_instance_stats()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getactivityinstancestats_raises_pycamunda_exception(engine_url):
    get_instance_stats = pycamunda.processdef.GetActivityInstanceStats(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_instance_stats()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.processdef.ActivityStats', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getactivityinstancestats_raises_for_status(mock, engine_url):
    get_instance_stats = pycamunda.processdef.GetActivityInstanceStats(url=engine_url, id_='anId')
    get_instance_stats()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getactivityinstancestats_returns_activitystats(engine_url):
    get_instance_stats = pycamunda.processdef.GetActivityInstanceStats(url=engine_url, id_='anId')
    instance_stats = get_instance_stats()

    assert isinstance(instance_stats, tuple)
    assert all(isinstance(stats, pycamunda.processdef.ActivityStats) for stats in instance_stats)
