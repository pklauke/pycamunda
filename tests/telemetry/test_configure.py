# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.telemetry
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_configure_params(engine_url):
    configure_telemetry = pycamunda.telemetry.Configure(url=engine_url, enable_telemetry=True)

    assert configure_telemetry.url == engine_url + '/telemetry/configuration'
    assert configure_telemetry.query_parameters() == {}
    assert configure_telemetry.body_parameters() == {'enableTelemetry': True}


@unittest.mock.patch('requests.Session.request')
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
def test_configure_calls_requests(mock, engine_url):
    configure_telemetry = pycamunda.telemetry.Configure(url=engine_url, enable_telemetry=True)
    configure_telemetry()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_configure_raises_pycamunda_exception(engine_url):
    configure_telemetry = pycamunda.telemetry.Configure(url=engine_url, enable_telemetry=True)
    with pytest.raises(pycamunda.PyCamundaException):
        configure_telemetry()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_configure_raises_for_status(mock, engine_url):
    configure_telemetry = pycamunda.telemetry.Configure(url=engine_url, enable_telemetry=True)
    configure_telemetry()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_configure_returns_none(engine_url):
    configure_telemetry = pycamunda.telemetry.Configure(url=engine_url, enable_telemetry=True)
    result = configure_telemetry()

    assert result is None
