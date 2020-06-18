# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.task


def test_task_load(my_task_json):
    user = pycamunda.task.Task.load(data=my_task_json)

    assert isinstance(user, pycamunda.task.Task)


def test_user_load_raises_key_error(my_task_json):
    for key in my_task_json:
        json_ = dict(my_task_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.task.Task.load(data=json_)
