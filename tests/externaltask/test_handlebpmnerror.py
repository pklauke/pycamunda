# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.externaltask
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_handlebpmnerror_params(engine_url):
    handle_error = pycamunda.externaltask.HandleBPMNError(
        url=engine_url,
        worker_id='1',
        id_='anId',
        error_code='anErrorCode',
        error_message='anErrorMessage'
    )
    handle_error.add_variable(name='aVar', value='aVal', type_='String', value_info={})

    assert handle_error.url == engine_url + '/external-task/anId/bpmnError'
    assert handle_error.query_parameters() == {}
    assert handle_error.body_parameters() == {
        'workerId': '1',
        'errorCode': 'anErrorCode',
        'errorMessage': 'anErrorMessage',
        'variables': {'aVar': {'value': 'aVal', 'type': 'String', 'valueInfo': {}}},
        }


@unittest.mock.patch('requests.post')
def test_handlebpmnerror_calls_requests(mock, engine_url):
    handle_error = pycamunda.externaltask.HandleBPMNError(
        url=engine_url, worker_id='1', id_='anId', error_code='anErrorCode'
    )
    handle_error()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_handlebpmnerror_raises_pycamunda_exception(engine_url):
    handle_error = pycamunda.externaltask.HandleBPMNError(
        url=engine_url, worker_id='1', id_='anId', error_code='anErrorCode'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        handle_error()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_handlebpmnerror_raises_for_status(mock, engine_url):
    handle_error = pycamunda.externaltask.HandleBPMNError(
        url=engine_url, worker_id='1', id_='anId', error_code='anErrorCode'
    )
    handle_error()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_handlebpmnerror_returns_none(engine_url):
    handle_error = pycamunda.externaltask.HandleBPMNError(
        url=engine_url, worker_id='1', id_='anId', error_code='anErrorCode'
    )
    result = handle_error()

    assert result is None
