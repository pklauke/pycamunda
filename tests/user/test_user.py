# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.user
import pycamunda.resource


def test_user_load(mary_doe_json):
    user = pycamunda.user.User.load(data=mary_doe_json)

    assert isinstance(user, pycamunda.user.User)
    assert user.id_ == mary_doe_json['id']
    assert user.first_name == mary_doe_json['firstName']
    assert user.last_name == mary_doe_json['lastName']
    assert user.email == mary_doe_json['email']


def test_user_load_raises_key_error():
    with pytest.raises(KeyError):
        pycamunda.user.User.load(data={
            'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@email.com'
        })
    with pytest.raises(KeyError):
        pycamunda.user.User.load(data={
            'id': 'janedoe', 'lastName': 'Doe', 'email': 'jane.doe@email.com'
        })
    with pytest.raises(KeyError):
        pycamunda.user.User.load(data={
            'id': 'janedoe', 'firstName': 'Jane', 'email': 'jane.doe@email.com'
        })
    pycamunda.user.User.load(data={
        'id': 'janedoe', 'firstName': 'Jane', 'lastName': 'Doe'
    })
    pycamunda.user.User.load(data={
        'id': 'janedoe', 'firstName': 'Jane', 'lastName': 'Doe', 'displayName': 'Jane Doe'
    })
