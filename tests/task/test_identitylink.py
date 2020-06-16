# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.task
import pycamunda.resource


def test_identitylink_load(my_identitylink_json):
    link = pycamunda.task.IdentityLink.load(data=my_identitylink_json)

    assert isinstance(link, pycamunda.task.IdentityLink)
    assert link.user_id == my_identitylink_json['userId']
    assert link.group_id == my_identitylink_json['groupId']
    assert link.type_ == my_identitylink_json['type']


def test_identitylink_load_raises_key_error(my_identitylink_json):
    for key in my_identitylink_json:
        json_ = dict(my_identitylink_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.task.IdentityLink.load(json_)
