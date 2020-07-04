# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_handlefailure_params(engine_url):
    handle_failure = pycamunda.externaltask.HandleFailure(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_message='anErrorMessage',
        error_details='anErrorDetail',
        retries=1,
        retry_timeout=10000
    )

    assert handle_failure.url == engine_url + '/external-task/anId/failure'
    assert handle_failure.query_parameters() == {}
    assert handle_failure.body_parameters() == {
        'workerId': '1',
        'errorMessage': 'anErrorMessage',
        'errorDetails': 'anErrorDetail',
        'retries': 1,
        'retryTimeout': 10000
    }


@unittest.mock.patch('requests.Session.request')
def test_handlefailure_calls_requests(mock, engine_url):
    handle_failure = pycamunda.externaltask.HandleFailure(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_message='anErrorMessage',
        error_details='anErrorDetail',
        retries=1,
        retry_timeout=10000
    )
    handle_failure()

    assert mock.called
    assert mock.call_args[1]['method'] == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_handlefailure_raises_pycamunda_exception(engine_url):
    handle_failure = pycamunda.externaltask.HandleFailure(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_message='anErrorMessage',
        error_details='anErrorDetail',
        retries=1,
        retry_timeout=10000
    )
    with pytest.raises(pycamunda.PyCamundaException):
        handle_failure()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_handlefailure_raises_for_status(mock, engine_url):
    handle_failure = pycamunda.externaltask.HandleFailure(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_message='anErrorMessage',
        error_details='anErrorDetail',
        retries=1,
        retry_timeout=10000
    )
    handle_failure()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_handlefailure_returns_none(engine_url):
    handle_failure = pycamunda.externaltask.HandleFailure(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_message='anErrorMessage',
        error_details='anErrorDetail',
        retries=1,
        retry_timeout=10000
    )
    result = handle_failure()

    assert result is None
