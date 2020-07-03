# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getlist_params(engine_url, getlist_input, getlist_output):
    get_tasks = pycamunda.task.GetList(url=engine_url, **getlist_input)

    assert get_tasks.url == engine_url + '/task'
    assert get_tasks.query_parameters() == getlist_output
    assert get_tasks.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.Task.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_getlist_calls_requests(mock, engine_url):
    get_tasks = pycamunda.task.GetList(url=engine_url)
    get_tasks()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_tasks = pycamunda.task.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_tasks()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.task.Task', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_tasks = pycamunda.task.GetList(url=engine_url)
    get_tasks()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat')
def test_getlist_returns_group(engine_url):
    get_tasks = pycamunda.task.GetList(url=engine_url)
    tasks = get_tasks()

    assert isinstance(tasks, tuple)
    assert all(isinstance(task, pycamunda.task.Task) for task in tasks)
