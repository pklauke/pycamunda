# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_filter_json():
    return {
        'id': 'anId',
        'resourceType': 'aResourceType',
        'name': 'aName',
        'owner': 'anOwner',
        'query': {'query_var': 'query_val'},
        'properties': {'prop_var': 'prop_val'},
        'itemCount': 1
    }


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'name': 'aName',
        'name_like': 'aNam',
        'owner': 'anOwner',
        'item_count': True,
        'sort_by': 'id_',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'filterId': 'anId',
        'name': 'aName',
        'nameLike': 'aNam',
        'owner': 'anOwner',
        'itemCount': 'true',
        'sortBy': 'filterId',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10,
        'resourceType': 'Task'
    }


@pytest.fixture
def count_input():
    return {
        'id_': 'anId',
        'name': 'aName',
        'name_like': 'aNam',
        'owner': 'anOwner',
    }


@pytest.fixture
def count_output():
    return {
        'filterId': 'anId',
        'name': 'aName',
        'nameLike': 'aNam',
        'owner': 'anOwner',
        'resourceType': 'Task'
    }
