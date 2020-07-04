# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_claim_params(engine_url):
    claim_task = pycamunda.task.Claim(url=engine_url, id_='anId', user_id='anUserId')

    assert claim_task.url == engine_url + '/task/anId/claim'
    assert claim_task.query_parameters() == {}
    assert claim_task.body_parameters() == {'userId': 'anUserId'}


@unittest.mock.patch('requests.Session.request')
def test_claim_calls_requests(mock, engine_url):
    claim_task = pycamunda.task.Claim(url=engine_url, id_='anId', user_id='anUserId')
    claim_task()

    assert mock.called
    assert mock.call_args[1]['method'] == 'POST'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_claim_raises_pycamunda_exception(engine_url):
    claim_task = pycamunda.task.Claim(url=engine_url, id_='anId', user_id='anUserId')
    with pytest.raises(pycamunda.PyCamundaException):
        claim_task()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_claim_raises_for_status(mock, engine_url):
    claim_task = pycamunda.task.Claim(url=engine_url, id_='anId', user_id='anUserId')
    claim_task()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_claim_returns_none(engine_url):
    claim_task = pycamunda.task.Claim(url=engine_url, id_='anId', user_id='anUserId')
    result = claim_task()

    assert result is None
