# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
import pycamunda.variable
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_setassignee_params(engine_url):
    set_task_assignee = pycamunda.task.SetAssignee(url=engine_url, id_='anId', user_id='anUserId')

    assert set_task_assignee.url == engine_url + '/task/anId/assignee'
    assert set_task_assignee.query_parameters() == {}
    assert set_task_assignee.body_parameters() == {'userId': 'anUserId'}


@unittest.mock.patch('requests.post')
def test_setassignee_calls_requests(mock, engine_url):
    set_task_assignee = pycamunda.task.SetAssignee(url=engine_url, id_='anId', user_id='anUserId')
    set_task_assignee()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_setassignee_raises_pycamunda_exception(engine_url):
    set_task_assignee = pycamunda.task.SetAssignee(url=engine_url, id_='anId', user_id='anUserId')
    with pytest.raises(pycamunda.PyCamundaException):
        set_task_assignee()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_setassignee_raises_for_status(mock, engine_url):
    set_task_assignee = pycamunda.task.SetAssignee(url=engine_url, id_='anId', user_id='anUserId')
    set_task_assignee()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_setassignee_returns_none(engine_url):
    set_task_assignee = pycamunda.task.SetAssignee(url=engine_url, id_='anId', user_id='anUserId')
    result = set_task_assignee()

    assert result is None
