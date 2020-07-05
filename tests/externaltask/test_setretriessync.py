# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_setretriessync_params(engine_url):
    set_retries = pycamunda.externaltask.SetRetriesSync(
        url=engine_url, external_task_ids=['anId'], retries=10
    )
    set_retries.process_instance_ids = ['anInstanceId']
    set_retries.external_task_query = 'aQuery'
    set_retries.process_instance_query = 'anInstanceQuery'
    set_retries.historic_process_instance_query = 'anHistoricQuery'

    assert set_retries.url == engine_url + '/external-task/retries'
    assert set_retries.query_parameters() == {}
    assert set_retries.body_parameters() == {
        'retries': 10,
        'externalTaskIds': ['anId'],
        'processInstanceIds': ['anInstanceId'],
        'externalTaskQuery': 'aQuery',
        'processInstanceQuery': 'anInstanceQuery',
        'historicProcessInstanceQuery': 'anHistoricQuery'
    }


@unittest.mock.patch('requests.Session.request')
def test_setretriessync_calls_requests(mock, engine_url):
    set_retries = pycamunda.externaltask.SetRetriesSync(
        url=engine_url, external_task_ids=['anId'], retries=10
    )
    set_retries()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_setretriessync_raises_pycamunda_exception(engine_url):
    set_retries = pycamunda.externaltask.SetRetriesSync(
        url=engine_url, external_task_ids=['anId'], retries=10
    )
    with pytest.raises(pycamunda.PyCamundaException):
        set_retries()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_setretriessync_raises_for_status(mock, engine_url):
    set_retries = pycamunda.externaltask.SetRetriesSync(
        url=engine_url, external_task_ids=['anId'], retries=10
    )
    set_retries()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_setretriessync_returns_none(engine_url):
    set_retries = pycamunda.externaltask.SetRetriesSync(
        url=engine_url, external_task_ids=['anId'], retries=10
    )
    result = set_retries()

    assert result is None
