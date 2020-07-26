# -*- coding: utf-8 -*-

import pytest

import pycamunda.identity
import pycamunda.group
import pycamunda.user


def test_group_load():
    users_groups = pycamunda.identity.UsersGroups.load({
        'groups': [{'id': 'anId', 'name': 'aName', 'type': 'String'}],
        'groupUsers': [
            {'id': 'janedoe', 'lastName': 'Doe', 'firstName': 'Jane', 'displayName': 'Jane Doe'}
        ]
    })

    assert all(isinstance(group, pycamunda.group.Group) for group in users_groups.groups)
    assert all(isinstance(user, pycamunda.user.User) for user in users_groups.group_users)


def test_group_load_raises_keyerror():
    users_groups_json = {'groups': [], 'groupUsers': []}
    for key in users_groups_json:
        json_ = dict(users_groups_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.group.Group.load(json_)
