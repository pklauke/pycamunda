# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_activate_params(engine_url):
    activate_instance = pycamunda.processinst.Activate(url=engine_url, id_='anId')

    assert activate_instance.url == engine_url + '/process-instance/anId/suspended'
    assert activate_instance.query_parameters() == {}
    assert activate_instance.body_parameters() == {'suspended': False}


@unittest.mock.patch('requests.put')
def test_activate_calls_requests(mock, engine_url):
    activate_instance = pycamunda.processinst.Activate(url=engine_url, id_='anId')
    activate_instance()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_activate_raises_pycamunda_exception(engine_url):
    activate_instance = pycamunda.processinst.Activate(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        activate_instance()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_activate_raises_for_status(mock, engine_url):
    activate_instance = pycamunda.processinst.Activate(url=engine_url, id_='anId')
    activate_instance()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_activate_returns_none(engine_url):
    activate_instance = pycamunda.processinst.Activate(url=engine_url, id_='anId')
    result = activate_instance()

    assert result is None


def test_suspend_params(engine_url):
    suspend_instance = pycamunda.processinst.Suspend(url=engine_url, id_='anId')

    assert suspend_instance.url == engine_url + '/process-instance/anId/suspended'
    assert suspend_instance.query_parameters() == {}
    assert suspend_instance.body_parameters() == {'suspended': True}


@unittest.mock.patch('requests.put')
def test_suspend_calls_requests(mock, engine_url):
    suspend_instance = pycamunda.processinst.Suspend(url=engine_url, id_='anId')
    suspend_instance()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_suspend_raises_pycamunda_exception(engine_url):
    suspend_instance = pycamunda.processinst.Suspend(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        suspend_instance()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_suspend_raises_for_status(mock, engine_url):
    suspend_instance = pycamunda.processinst.Suspend(url=engine_url, id_='anId')
    suspend_instance()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_suspend_returns_none(engine_url):
    suspend_instance = pycamunda.processinst.Suspend(url=engine_url, id_='anId')
    result = suspend_instance()

    assert result is None
