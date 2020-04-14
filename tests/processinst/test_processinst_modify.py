# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
import pycamunda.batch
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_modify_params_default(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'instructions': []
    }


def test_modify_params_non_default(engine_url):
    modify_instance = pycamunda.processinst.Modify(
        url=engine_url,
        id_='anInstanceId',
        skip_custom_listeners=True,
        skip_io_mappings=True
    )

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': True,
        'skipIoMappings': True,
        'instructions': []
    }


def test_modify_params_async(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId', async_=True)

    assert modify_instance.url == engine_url + '/process-instance/anInstanceId/modification-async'
    assert modify_instance.query_parameters() == {}
    assert modify_instance.body_parameters() == {
        'skipCustomListeners': False,
        'skipIoMappings': False,
        'instructions': []
    }


@unittest.mock.patch('requests.post')
def test_modify_calls_requests(mock, engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_modify_raises_pycamunda_exception(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    with pytest.raises(pycamunda.PyCamundaException):
        modify_instance()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_modify_raises_for_status(mock, engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    modify_instance()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_modify_returns_none(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId')
    result = modify_instance()

    assert result is None


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_modify_async_returns_batch(engine_url):
    modify_instance = pycamunda.processinst.Modify(url=engine_url, id_='anInstanceId', async_=True)
    batch = modify_instance()

    assert isinstance(batch, pycamunda.batch.Batch)


# TODO add tests for instructions
