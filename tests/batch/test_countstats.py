# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock, count_response_mock


def test_countstats_params(engine_url, count_input, count_output):
    count_batch_stats = pycamunda.batch.CountStats(url=engine_url, **count_input)

    assert count_batch_stats.url == engine_url + '/batch/statistics/count'
    assert count_batch_stats.query_parameters() == count_output
    assert count_batch_stats.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_countstats_calls_requests(mock, engine_url):
    count_batch_stats = pycamunda.batch.CountStats(url=engine_url)
    count_batch_stats()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_countstats_raises_pycamunda_exception(engine_url):
    count_batch_stats = pycamunda.batch.CountStats(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_batch_stats()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_countstats_raises_for_status(mock, engine_url):
    count_batch_stats = pycamunda.batch.CountStats(url=engine_url)
    count_batch_stats()

    assert mock.called


@unittest.mock.patch('requests.Session.request', count_response_mock)
def test_countstats_returns_int(engine_url):
    count_batch_stats = pycamunda.batch.CountStats(url=engine_url)
    result = count_batch_stats()

    assert isinstance(result, int)
