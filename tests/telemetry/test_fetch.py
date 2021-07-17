# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.telemetry
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, fetch_response_mock


def test_fetch_params(engine_url):
    enable_telemetry = pycamunda.telemetry.Fetch(url=engine_url)

    assert enable_telemetry.url == engine_url + '/telemetry/configuration'
    assert enable_telemetry.query_parameters() == {}
    assert enable_telemetry.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
@unittest.mock.patch('pycamunda.processinst.ProcessInstance', unittest.mock.MagicMock())
def test_fetch_calls_requests(mock, engine_url):
    enable_telemetry = pycamunda.telemetry.Fetch(url=engine_url)
    enable_telemetry()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_fetch_raises_pycamunda_exception(engine_url):
    enable_telemetry = pycamunda.telemetry.Fetch(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        enable_telemetry()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_fetch_raises_for_status(mock, engine_url):
    enable_telemetry = pycamunda.telemetry.Fetch(url=engine_url)
    enable_telemetry()

    assert mock.called


@unittest.mock.patch('requests.Session.request', fetch_response_mock)
def test_fetch_returns_bool(engine_url):
    fetch_telemetry = pycamunda.telemetry.Fetch(url=engine_url)
    enable_telemetry = fetch_telemetry()

    assert isinstance(enable_telemetry, bool)
