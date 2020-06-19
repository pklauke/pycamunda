# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.task


def test_comment_load(my_comment_json):
    user = pycamunda.task.Comment.load(data=my_comment_json)

    assert isinstance(user, pycamunda.task.Comment)


def test_comment_load_raises_key_error(my_comment_json):
    for key in my_comment_json:
        json_ = dict(my_comment_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.task.Comment.load(data=json_)
