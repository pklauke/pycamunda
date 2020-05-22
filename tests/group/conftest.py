# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def getlist_input():
    return {
        'id_': 'anId',
        'id_in': [],
        'name': 'aName',
        'name_like': [],
        'type_': 'aType',
        'member': 'aMember',
        'member_of_tenant': 'aMemberOfTenant',
        'sort_by': 'id_',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def getlist_output():
    return {
        'id': 'anId',
        'idIn': [],
        'name': 'aName',
        'nameLike': [],
        'type': 'aType',
        'member': 'aMember',
        'memberOfTenant': 'aMemberOfTenant',
        'sortBy': 'id',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }
