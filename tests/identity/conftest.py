# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_users_groups_json():
    return {
        'groups': [{'id': 'anId', 'name': 'aName', 'type': 'String'}],
        'groupUsers': [
            {'id': 'janedoe', 'lastName': 'Doe', 'firstName': 'Jane', 'displayName': 'Jane Doe'}
        ]
    }


@pytest.fixture
def my_auth_status_json():
    return {
        'authenticatedUser': 'anId',
        'authenticated': True
    }


@pytest.fixture
def my_passwordpolicy_json():
    return {
        'placeholder': 'aPlaceholder',
        'parameters': {'minChars': '1'}
    }


@pytest.fixture
def my_passwordpolicycompliance_json():
    return {
        'placeholder': 'aPlaceholder',
        'parameters': {'minChars': '1'},
        'valid': True
    }
