# -*- coding: utf-8 -*-

import datetime as dt
import unittest.mock

import pytest

import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_activate_params(engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')

    assert activate_batch.url == engine_url + '/batch/anId/suspended'
    assert activate_batch.query_parameters() == {}
    assert activate_batch.body_parameters() == {'suspended': False}


def test_activate_path(engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')

    assert activate_batch.url == engine_url + '/batch/anId/suspended'


@unittest.mock.patch('requests.Session.request')
def test_activate_calls_requests(mock, engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')
    activate_batch()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_activate_raises_pycamunda_exception(engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        activate_batch()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_activate_raises_for_status(mock, engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')
    activate_batch()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_activate_returns_none(engine_url):
    activate_batch = pycamunda.batch.Activate(url=engine_url, id_='anId')
    result = activate_batch()

    assert result is None


def test_suspend_params(engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')

    assert suspend_batch.url == engine_url + '/batch/anId/suspended'
    assert suspend_batch.query_parameters() == {}
    assert suspend_batch.body_parameters() == {'suspended': True}


def test_suspend_path(engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')

    assert suspend_batch.url == engine_url + '/batch/anId/suspended'


@unittest.mock.patch('requests.Session.request')
def test_suspend_calls_requests(mock, engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')
    suspend_batch()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_suspend_raises_pycamunda_exception(engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        suspend_batch()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_suspend_raises_for_status(mock, engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')
    suspend_batch()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_suspend_returns_none(engine_url):
    suspend_batch = pycamunda.batch.Suspend(url=engine_url, id_='anId')
    result = suspend_batch()

    assert result is None
