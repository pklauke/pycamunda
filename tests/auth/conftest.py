# -*- coding: utf-8 -*-

import pytest

import pycamunda.resource
import pycamunda.auth


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


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'type_': 0,
        'user_id_in': ['anUser'],
        'group_id_in': ['aGroup'],
        'resource_type': 1,
        'sort_by': 'resource_type',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'id': 'anId',
        'type': pycamunda.auth.AuthorizationType(0).value,
        'userIdIn': ['anUser'],
        'groupIdIn': ['aGroup'],
        'resourceType': pycamunda.resource.ResourceType(1).value,
        'sortBy': 'resourceType',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def count_input():
    return {
        'id_': 'anId',
        'type_': 0,
        'user_id_in': ['anUser'],
        'group_id_in': ['aGroup'],
        'resource_type': 1
    }


@pytest.fixture
def count_output():
    return {
        'id': 'anId',
        'type': pycamunda.auth.AuthorizationType(0).value,
        'userIdIn': ['anUser'],
        'groupIdIn': ['aGroup'],
        'resourceType': pycamunda.resource.ResourceType(1).value
    }


@pytest.fixture
def check_input():
    return {
        'permission_name': 'READ',
        'permission_value': 1,
        'resource_name': 'USER',
        'resource_type': 1,
        'resource_id': 'demo'
    }


@pytest.fixture
def check_output():
    return {
        'permissionName': 'READ',
        'permissionValue': 1,
        'resourceName': 'USER',
        'resourceType': 1,
        'resourceId': 'demo'
    }


@pytest.fixture
def create_input():
    return {
        'type_': 0,
        'permissions': ['CREATE'],
        'user_id': 'anId',
        'resource_type': 1,
        'resource_id': 'demo'
    }


@pytest.fixture
def create_output():
    return {
        'type': 0,
        'permissions': ['CREATE'],
        'userId': 'anId',
        'resourceType': 1,
        'resourceId': 'demo'
    }


@pytest.fixture
def update_input():
    return {
        'id_': 'anId',
        'permissions': ['CREATE'],
        'user_id': 'anId',
        'resource_type': 1,
        'resource_id': 'demo'
    }


@pytest.fixture
def update_output():
    return {
        'permissions': ['CREATE'],
        'userId': 'anId',
        'resourceType': 1,
        'resourceId': 'demo'
    }
