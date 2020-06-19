# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_commentget_params(engine_url):
    get_comment = pycamunda.task.CommentGet(url=engine_url, task_id='anId', comment_id='anotherId')

    assert get_comment.url == engine_url + '/task/anId/comment/anotherId'
    assert get_comment.query_parameters() == {}
    assert get_comment.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.get')
def test_commentget_calls_requests(mock, engine_url, task_input):
    get_comment = pycamunda.task.CommentGet(url=engine_url, task_id='anId', comment_id='anotherId')
    get_comment()

    assert mock.called


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_commentget_raises_pycamunda_exception(engine_url, task_input):
    get_comment = pycamunda.task.CommentGet(url=engine_url, task_id='anId', comment_id='anotherId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_comment()


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_commentget_raises_for_status(mock, engine_url, task_input):
    get_comment = pycamunda.task.CommentGet(url=engine_url, task_id='anId', comment_id='anotherId')
    get_comment()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_commentget_returns_comment(engine_url, task_input):
    get_comment = pycamunda.task.CommentGet(url=engine_url, task_id='anId', comment_id='anotherId')
    comment = get_comment()

    assert isinstance(comment, pycamunda.task.Comment)
