# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_batches = pycamunda.batch.GetList(url=engine_url, **getlist_input)

    assert get_batches.url == engine_url + '/batch'
    assert get_batches.query_parameters() == getlist_output
    assert get_batches.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests(mock, engine_url):
    get_batches = pycamunda.batch.GetList(url=engine_url)
    get_batches()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_batches = pycamunda.batch.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_batches()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.batch.Batch', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_batches = pycamunda.batch.GetList(url=engine_url)
    get_batches()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getlist_returns_batches(engine_url):
    get_batches = pycamunda.batch.GetList(url=engine_url)
    batches = get_batches()

    assert isinstance(batches, tuple)
    assert all(isinstance(batch, pycamunda.batch.Batch) for batch in batches)
