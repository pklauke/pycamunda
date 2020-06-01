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
