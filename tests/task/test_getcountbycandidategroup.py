# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_getcountbycandidategroup_params(engine_url):
    get_task_counts = pycamunda.task.GetCountByCandidateGroup(url=engine_url)

    assert get_task_counts.url == engine_url + '/task/report/candidate-group-count'
    assert get_task_counts.query_parameters() == {}
    assert get_task_counts.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.CountByCandidateGroup.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_getcountbycandidategroup_calls_requests(mock, engine_url):
    get_task_counts = pycamunda.task.GetCountByCandidateGroup(url=engine_url)
    get_task_counts()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_getcountbycandidategroup_raises_pycamunda_exception(engine_url):
    get_task_counts = pycamunda.task.GetCountByCandidateGroup(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_task_counts()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.task.CountByCandidateGroup', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getcountbycandidategroup_raises_for_status(mock, engine_url):
    get_task_counts = pycamunda.task.GetCountByCandidateGroup(url=engine_url)
    get_task_counts()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_getcountbycandidategroup_returns_coundbycandidategroup(engine_url):
    get_task_counts = pycamunda.task.GetCountByCandidateGroup(url=engine_url)
    task_counts = get_task_counts()

    assert all(
        isinstance(task_count, pycamunda.task.CountByCandidateGroup) for task_count in task_counts
    )
