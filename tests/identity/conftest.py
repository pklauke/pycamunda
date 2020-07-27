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
