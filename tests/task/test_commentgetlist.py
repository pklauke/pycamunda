# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_commentgetlist_params(engine_url):
    get_comments = pycamunda.task.CommentGetList(url=engine_url, task_id='anId')

    assert get_comments.url == engine_url + '/task/anId/comment'
    assert get_comments.query_parameters() == {}
    assert get_comments.body_parameters() == {}


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request')
def test_commentgetlist_calls_requests(mock, engine_url, task_input):
    get_comments = pycamunda.task.CommentGetList(url=engine_url, task_id='anId')
    get_comments()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'GET'


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_commentgetlist_raises_pycamunda_exception(engine_url, task_input):
    get_comments = pycamunda.task.CommentGetList(url=engine_url, task_id='anId')
    with pytest.raises(pycamunda.PyCamundaException):
        get_comments()


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_commentgetlist_raises_for_status(mock, engine_url, task_input):
    get_comments = pycamunda.task.CommentGetList(url=engine_url, task_id='anId')
    get_comments()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
def test_commentgetlist_returns_comment(engine_url, task_input):
    get_comments = pycamunda.task.CommentGetList(url=engine_url, task_id='anId')
    comments = get_comments()

    assert isinstance(comments, tuple)
    assert all(isinstance(comment, pycamunda.task.Comment) for comment in comments)
