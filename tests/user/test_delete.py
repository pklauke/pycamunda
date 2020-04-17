# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_delete_params(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')

    assert delete_user.url == engine_url + '/user/myuserid'
    assert delete_user.query_parameters() == {}
    assert delete_user.body_parameters() == {}


@unittest.mock.patch('requests.delete')
def test_delete_calls_requests(mock, engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    delete_user()

    assert mock.called


@unittest.mock.patch('requests.delete', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_user()


@unittest.mock.patch('requests.delete', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    delete_user()

    assert mock.called


@unittest.mock.patch('requests.delete', unittest.mock.MagicMock())
def test_delete_returns_none(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    result = delete_user()

    assert result is None
