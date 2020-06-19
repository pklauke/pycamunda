# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.task
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_commentcreate_params(engine_url):
    create_comment = pycamunda.task.CommentCreate(
        url=engine_url, task_id='anId', message='aMessage'
    )

    assert create_comment.url == engine_url + '/task/anId/comment/create'
    assert create_comment.query_parameters() == {}
    assert create_comment.body_parameters() == {'message': 'aMessage'}


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.post')
def test_commentcreate_calls_requests(mock, engine_url):
    create_comment = pycamunda.task.CommentCreate(
        url=engine_url, task_id='anId', message='aMessage'
    )
    create_comment()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_commentcreate_raises_pycamunda_exception(engine_url):
    create_comment = pycamunda.task.CommentCreate(
        url=engine_url, task_id='anId', message='aMessage'
    )
    with pytest.raises(pycamunda.PyCamundaException):
        create_comment()


@unittest.mock.patch('pycamunda.task.Comment.load', unittest.mock.MagicMock())
@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_commentcreate_raises_for_status(mock, engine_url):
    create_comment = pycamunda.task.CommentCreate(
        url=engine_url, task_id='anId', message='aMessage'
    )
    create_comment()

    assert mock.called


@unittest.mock.patch('pycamunda.base.from_isoformat', unittest.mock.MagicMock())
@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_commentcreate_returns_comment(engine_url):
    create_comment = pycamunda.task.CommentCreate(
        url=engine_url, task_id='anId', message='aMessage'
    )
    comment = create_comment()

    assert isinstance(comment, pycamunda.task.Comment)
