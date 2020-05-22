# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.group
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_delete_params(engine_url):
    delete_group = pycamunda.group.Delete(url=engine_url, id_='anId')

    assert delete_group.url == engine_url + '/group/anId'
    assert delete_group.query_parameters() == {}
    assert delete_group.body_parameters() == {}


@unittest.mock.patch('requests.delete')
def test_delete_calls_requests(mock, engine_url):
    delete_group = pycamunda.group.Delete(url=engine_url, id_='anId')
    delete_group()

    assert mock.called


@unittest.mock.patch('requests.delete', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url):
    delete_group = pycamunda.group.Delete(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_group()


@unittest.mock.patch('requests.delete', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url):
    delete_group = pycamunda.group.Delete(url=engine_url, id_='anId')
    delete_group()

    assert mock.called


@unittest.mock.patch('requests.delete', unittest.mock.MagicMock())
def test_delete_returns_group(engine_url):
    delete_group = pycamunda.group.Delete(url=engine_url, id_='anId')
    result = delete_group()

    assert result is None
