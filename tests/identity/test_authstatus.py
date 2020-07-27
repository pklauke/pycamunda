# -*- coding: utf-8 -*-

import pytest

import pycamunda.identity
import pycamunda.group
import pycamunda.user


def test_authstatus_load(my_auth_status_json):
    auth_status = pycamunda.identity.AuthStatus.load(my_auth_status_json)

    assert auth_status.user_id == my_auth_status_json['authenticatedUser']
    assert auth_status.authenticated == my_auth_status_json['authenticated']


def test_authstatus_load_raises_keyerror(my_auth_status_json):
    for key in my_auth_status_json:
        json_ = dict(my_auth_status_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.identity.AuthStatus.load(json_)
