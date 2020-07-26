# -*- coding: utf-8 -*-

import pytest

import pycamunda.group


def test_group_load():
    batch = pycamunda.group.Group.load({'id': 'anId', 'name': 'aName', 'type': 'String'})

    assert batch.id_ == 'anId'
    assert batch.name == 'aName'
    assert batch.type_ == 'String'


def test_group_load_raises_keyerror():
    group_json = {'id': 'anId', 'name': 'aName'}
    for key in group_json:
        json_ = dict(group_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.group.Group.load(json_)
    pycamunda.group.Group.load({**group_json, 'type': 'String'})
