# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_profile_params(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)

    assert update_profile.url == engine_url + '/user/janedoe/profile'
    assert update_profile.query_parameters() == {}
    assert update_profile.body_parameters() == {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }


@unittest.mock.patch('requests.put')
def test_update_profile_calls_requests(mock, engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    update_profile()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_update_profile_raises_pycamunda_exception(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)

    with pytest.raises(pycamunda.PyCamundaException):
        update_profile()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_profile_raises_for_status(mock, engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    update_profile()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_update_profile_returns_none(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    result = update_profile()

    assert result is None
