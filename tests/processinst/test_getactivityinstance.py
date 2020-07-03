# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.processinst
import pycamunda.activityinst
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getactivityinstance_params(engine_url):
    get_activity_instance = pycamunda.processinst.GetActivityInstance(url=engine_url, id_='anId')

    assert get_activity_instance.url == engine_url + '/process-instance/anId/activity-instances'
    assert get_activity_instance.query_parameters() == {}
    assert get_activity_instance.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_getactivityinstance_calls_requests(mock, engine_url):
    get_activity_instance = pycamunda.processinst.GetActivityInstance(url=engine_url, id_='anId')
    get_activity_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getactivityinstance_raises_pycamunda_exception(engine_url):
    get_activity_instance = pycamunda.processinst.GetActivityInstance(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_activity_instance()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.activityinst.ActivityInstance', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getactivityinstance_raises_for_status(mock, engine_url):
    get_activity_instance = pycamunda.processinst.GetActivityInstance(url=engine_url, id_='anId')
    get_activity_instance()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getactivityinstance_returns_none(engine_url):
    get_activity_instance = pycamunda.processinst.GetActivityInstance(url=engine_url, id_='anId')
    activity_instance = get_activity_instance()

    assert isinstance(activity_instance, pycamunda.activityinst.ActivityInstance)
