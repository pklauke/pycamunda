# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_authorization_json():
    return {
        'id': 'anId',
        'type': 0,
        'permissions': ['CREATE', 'READ'],
        'userId': 'anotherId',
        'groupId': 'aGroupId',
        'resourceType': 1,
        'resourceId': '*',
        'links': [{'method': 'GET', 'href': 'http://localhost/', 'rel': 'self'}],
        'removalTime': '2000-01-01T01:01:01.000+0000',
        'rootProcessInstanceId': 'anInstanceId'
    }
