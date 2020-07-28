# -*- coding: utf-8 -*-

import pytest

import pycamunda.identity
import pycamunda.group
import pycamunda.user


def test_passwordpolicy_load(my_passwordpolicy_json):
    password_policy = pycamunda.identity.PasswordPolicy.load(my_passwordpolicy_json)

    assert password_policy.placeholder == my_passwordpolicy_json['placeholder']
    assert password_policy.parameters == my_passwordpolicy_json['parameters']


def test_passwordpolicy_load_raises_keyerror(my_passwordpolicy_json):
    for key in my_passwordpolicy_json:
        json_ = dict(my_passwordpolicy_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.identity.PasswordPolicy.load(json_)
