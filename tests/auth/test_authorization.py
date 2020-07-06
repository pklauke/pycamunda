# -*- coding: utf-8 -*-

import datetime as dt

import pytest

import pycamunda.auth
import pycamunda.resource


def test_authorization_load(my_authorization_json):
    auth = pycamunda.auth.Authorization.load(my_authorization_json)

    assert auth.id_ == my_authorization_json['id']
    assert auth.type_ == my_authorization_json['type']
    assert auth.permissions == my_authorization_json['permissions']
    assert auth.user_id == my_authorization_json['userId']
    assert auth.group_id == my_authorization_json['groupId']
    assert auth.resource_type == my_authorization_json['resourceType']
    assert auth.resource_id == my_authorization_json['resourceId']
    assert all(isinstance(link, pycamunda.resource.Link) for link in auth.links)
    assert isinstance(auth.removal_time, dt.datetime)
    assert auth.root_process_instance_id == my_authorization_json['rootProcessInstanceId']


def test_authorization_load_raises_keyerror(my_authorization_json):
    for key in (k for k in my_authorization_json
                if k not in ('links', 'removalTime', 'rootProcessInstanceId')):
        json_ = dict(my_authorization_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.auth.Authorization.load(json_)

    for key in ('links', 'removalTime', 'rootProcessInstanceId'):
        json_ = dict(my_authorization_json)
        del json_[key]
        pycamunda.auth.Authorization.load(json_)
