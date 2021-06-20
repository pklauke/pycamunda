# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getstats_params(engine_url, getlist_input, getlist_output):
    get_batch_stats = pycamunda.batch.GetStats(url=engine_url, **getlist_input)

    assert get_batch_stats.url == engine_url + '/batch/statistics'
    assert get_batch_stats.query_parameters() == getlist_output
    assert get_batch_stats.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_getstats_calls_requests(mock, engine_url):
    get_batch_stats = pycamunda.batch.GetStats(url=engine_url)
    get_batch_stats()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getstats_raises_pycamunda_exception(engine_url):
    get_batch_stats = pycamunda.batch.GetStats(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_batch_stats()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.batch.BatchStats', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getstats_raises_for_status(mock, engine_url):
    get_batch_stats = pycamunda.batch.GetStats(url=engine_url)
    get_batch_stats()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getstats_returns_batchstats(engine_url):
    get_batch_stats = pycamunda.batch.GetStats(url=engine_url)
    batch_stats = get_batch_stats()

    assert isinstance(batch_stats, tuple)
    assert all(isinstance(batch_stats_, pycamunda.batch.BatchStats) for batch_stats_ in batch_stats)
