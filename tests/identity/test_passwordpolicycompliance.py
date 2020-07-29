# -*- coding: utf-8 -*-

import pytest

import pycamunda.identity
import pycamunda.group
import pycamunda.user


def test_passwordpolicycompliance_load(my_passwordpolicycompliance_json):
    policy_compliance = pycamunda.identity.PasswordPolicyCompliance.load(my_passwordpolicycompliance_json)

    assert policy_compliance.policy.placeholder == my_passwordpolicycompliance_json['placeholder']
    assert policy_compliance.policy.parameters == my_passwordpolicycompliance_json['parameters']
    assert policy_compliance.valid == my_passwordpolicycompliance_json['valid']


def test_passwordpolicycompliance_load_raises_keyerror(my_passwordpolicycompliance_json):
    for key in my_passwordpolicycompliance_json:
        json_ = dict(my_passwordpolicycompliance_json)
        del json_[key]
        with pytest.raises(KeyError):
            pycamunda.identity.PasswordPolicyCompliance.load(json_)
