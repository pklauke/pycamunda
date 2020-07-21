# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.task


def test_task_load(my_countbycandidategroup_json):
    task_counts = pycamunda.task.CountByCandidateGroup.load(data=my_countbycandidategroup_json)

    assert isinstance(task_counts, pycamunda.task.CountByCandidateGroup)


def test_task_load_raises_key_error(my_countbycandidategroup_json):
    for key in my_countbycandidategroup_json:
        json_ = dict(my_countbycandidategroup_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.task.CountByCandidateGroup.load(data=json_)
