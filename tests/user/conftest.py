# -*- coding: utf-8 -*-

import pytest

import pycamunda.user


@pytest.fixture
def mary_doe_json():
    return {
        'id': 'janedoe',
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }


@pytest.fixture
def john_doe_json():
    return {
        'id': 'johndoe',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@email.com'
    }


@pytest.fixture
def jane_doe_dict():
    return {
        'id_': 'janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@email.com'
    }


@pytest.fixture
def jane_doe():
    return pycamunda.user.User(
        id_='janedoe', first_name='Jane', last_name='Doe', email='jane.doe@email.com'
    )


@pytest.fixture
def count_input():
    return {
        'first_name': 'jane',
        'first_name_like': 'jan',
        'last_name': 'doe',
        'last_name_like': 'do',
        'email': 'jane.doe@email.com',
        'email_like': 'jan.doe@email.com',
        'member_of_group': 'mygroup',
        'member_of_tenant': 'mytenant'
    }


@pytest.fixture
def count_params():
    return {
        'firstName': 'jane',
        'firstNameLike': 'jan',
        'lastName': 'doe',
        'lastNameLike': 'do',
        'email': 'jane.doe@email.com',
        'emailLike': 'jan.doe@email.com',
        'memberOfGroup': 'mygroup',
        'memberOfTenant': 'mytenant'
    }


@pytest.fixture
def get_list_input():
    return {
        'first_name': 'jane',
        'first_name_like': 'jan',
        'last_name': 'doe',
        'last_name_like': 'do',
        'email': 'jane.doe@email.com',
        'email_like': 'jan.doe@email.com',
        'member_of_group': 'mygroup',
        'member_of_tenant': 'mytenant',
        'sort_by': 'id_',
        'ascending': False,
        'first_result': 1,
        'max_results': 10
    }


@pytest.fixture
def get_list_params():
    return {
        'firstName': 'jane',
        'firstNameLike': 'jan',
        'lastName': 'doe',
        'lastNameLike': 'do',
        'email': 'jane.doe@email.com',
        'emailLike': 'jan.doe@email.com',
        'memberOfGroup': 'mygroup',
        'memberOfTenant': 'mytenant',
        'sortBy': 'userId',
        'sortOrder': 'desc',
        'firstResult': 1,
        'maxResults': 10
    }


@pytest.fixture
def update_credentials_input():
    return {
        'id_': 'janedoe',
        'password': 'password',
        'authenticated_user_password': 'password'
    }
