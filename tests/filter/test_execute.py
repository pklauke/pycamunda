# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.filter
import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_execute_params(engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')

    assert execute_filter.url == engine_url + '/filter/anId/list'
    assert execute_filter.query_parameters() == {}
    assert execute_filter.body_parameters() == {}


def test_execute_params_single_reuslt(engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId', single_result=True)

    assert execute_filter.url == engine_url + '/filter/anId/singleResult'
    assert execute_filter.query_parameters() == {}
    assert execute_filter.body_parameters() == {}


@unittest.mock.patch('requests.Session.request')
def test_execute_calls_requests(mock, engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')
    execute_filter()

    assert mock.called


@unittest.mock.patch('requests.Session.request')
def test_execute_calls_requests_post(mock, engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')
    execute_filter.priority = 1
    execute_filter()

    assert mock.called


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_execute_raises_pycamunda_exception(engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        execute_filter()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.task.Task')
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_execute_raises_for_status(mock, engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')
    execute_filter()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_execute_returns_tasks(engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId')
    tasks = execute_filter()

    assert isinstance(tasks, tuple)
    assert all(isinstance(task, pycamunda.task.Task) for task in tasks)


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_execute_returns_task(engine_url):
    execute_filter = pycamunda.filter.Execute(url=engine_url, id_='anId', single_result=True)
    task = execute_filter()

    assert isinstance(task, pycamunda.task.Task)
