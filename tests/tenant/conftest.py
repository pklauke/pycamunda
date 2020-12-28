# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def get_list_input():
    return {
        'id_': 'anId',
        'name': 'aName',
        'name_like': 'aNam',
        'user_member': 'aUser',
        'group_member': 'aGroup',
        'including_groups_of_user': True,
        'sort_by': 'id_',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def get_list_output():
    return {
        'id': 'anId',
        'name': 'aName',
        'nameLike': 'aNam',
        'userMember': 'aUser',
        'groupMember': 'aGroup',
        'includingGroupsOfUser': True,
        'sortBy': 'id',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def count_input():
    return {
        'id_': 'anId',
        'name': 'aName',
        'name_like': 'aNam',
        'user_member': 'aUser',
        'group_member': 'aGroup',
        'including_groups_of_user': True
    }


@pytest.fixture
def count_output():
    return {
        'id': 'anId',
        'name': 'aName',
        'nameLike': 'aNam',
        'userMember': 'aUser',
        'groupMember': 'aGroup',
        'includingGroupsOfUser': True
    }
