# -*- coding: utf-8 -*-

import unittest.mock

import pytest
import requests

import pycamunda.base
import pycamunda.user
import pycamunda.resource


def raise_requests_exception_mock(*args, **kwargs):
    raise requests.exceptions.RequestException


def not_ok_response_mock(*args, **kwargs):
    class Response:
        ok = False
        text = ''

        def __bool__(self):
            return bool(self.ok)

        def json(self):
            return {'message': 'an error message'}

    return Response()


def count_response_mock(*args, **kwargs):
    class Response:
        ok = True

        def __bool__(self):
            return bool(self.ok)

        def json(self):
            return {'count': 1}

    return Response()


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
    with pytest.raises(KeyError):
        pycamunda.user.User.load(data={
            'id': 'janedoe', 'firstName': 'Jane', 'lastName': 'Doe'
        })


def test_delete_params(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')

    assert delete_user.url == engine_url + '/user/myuserid'
    assert delete_user.query_parameters() == {}
    assert delete_user.body_parameters() == {}


@unittest.mock.patch('requests.delete')
def test_delete_calls_requests(mock, engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    delete_user()

    assert mock.called


@unittest.mock.patch('requests.delete', raise_requests_exception_mock)
def test_delete_raises_pycamunda_exception(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    with pytest.raises(pycamunda.PyCamundaException):
        delete_user()


@unittest.mock.patch('requests.delete', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_delete_raises_for_status(mock, engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    delete_user()

    assert mock.called


@unittest.mock.patch('requests.delete', unittest.mock.MagicMock())
def test_delete_returns_none(engine_url):
    delete_user = pycamunda.user.Delete(url=engine_url, id_='myuserid')
    result = delete_user()

    assert result is None


def test_count_params(engine_url, count_input, count_params):
    count_users = pycamunda.user.Count(url=engine_url, **count_input)

    assert count_users.url == engine_url + '/user/count'
    assert count_users.body_parameters() == {}
    assert count_users.query_parameters() == count_params


@unittest.mock.patch('requests.get')
def test_count_calls_requests(mock, engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    count_users()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_count_raises_pycamunda_exception(engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        count_users()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_count_raises_for_status(mock, engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    with pytest.raises(KeyError):
        count_users()

    assert mock.called


@unittest.mock.patch('requests.get', count_response_mock)
def test_count_returns_int(engine_url):
    count_users = pycamunda.user.Count(url=engine_url)
    count = count_users()

    assert isinstance(count, int)


def test_getlist_params(engine_url, get_list_input, get_list_params):
    get_users = pycamunda.user.GetList(url=engine_url, **get_list_input)

    assert get_users.url == engine_url + '/user'
    assert get_users.body_parameters() == {}
    assert get_users.query_parameters() == get_list_params


@unittest.mock.patch('requests.get')
def test_getlist_calls_requests(mock, engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    get_users()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getlist_raises_pycamunda_exception(engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_users()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.user.User', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getlist_raises_for_status(mock, engine_url):
    get_users = pycamunda.user.GetList(url=engine_url)
    get_users()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
def test_getlist_returns_users(engine_url):
    get_users = pycamunda.user.GetList(url=engine_url, id_='myuserid')
    users = get_users()

    assert isinstance(users, tuple)
    assert all(isinstance(user, pycamunda.user.User) for user in users)


def test_getprofile_params(engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')

    assert get_profile.url == engine_url + '/user/myuserid/profile'
    assert get_profile.query_parameters() == {}
    assert get_profile.body_parameters() == {}


@unittest.mock.patch('requests.get')
def test_getprofile_calls_requests(mock, engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    get_profile()

    assert mock.called


@unittest.mock.patch('requests.get', raise_requests_exception_mock)
def test_getprofile_raises_pycamunda_exception(engine_url):
    get_profile = pycamunda.user.GetList(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_profile()


@unittest.mock.patch('requests.get', not_ok_response_mock)
@unittest.mock.patch('pycamunda.user.User', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_getprofile_raises_for_status(mock, engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    get_profile()

    assert mock.called


@unittest.mock.patch('requests.get', unittest.mock.MagicMock())
def test_getprofile_returns_user(engine_url):
    get_profile = pycamunda.user.GetProfile(url=engine_url, id_='myuserid')
    user_profile = get_profile()

    assert isinstance(user_profile, pycamunda.user.User)


def test_options_params(engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')

    assert get_options.url == engine_url + '/user/myuserid'
    assert get_options.query_parameters() == {}
    assert get_options.body_parameters() == {}


@unittest.mock.patch('requests.options')
def test_options_calls_requests(mock, engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    get_options()

    assert mock.called


@unittest.mock.patch('requests.options', raise_requests_exception_mock)
def test_options_raises_pycamunda_exception(engine_url):
    get_options = pycamunda.user.Options(url=engine_url)
    with pytest.raises(pycamunda.PyCamundaException):
        get_options()


@unittest.mock.patch('requests.options', not_ok_response_mock)
@unittest.mock.patch('pycamunda.resource.ResourceOptions', unittest.mock.MagicMock())
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_options_raises_for_status(mock, engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    get_options()

    assert mock.called


@unittest.mock.patch('requests.options', unittest.mock.MagicMock())
def test_options_returns_resource_options(engine_url):
    get_options = pycamunda.user.Options(url=engine_url, id_='myuserid')
    resource_options = get_options()

    assert isinstance(resource_options, pycamunda.resource.ResourceOptions)


def test_create_params(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')

    assert create_user.url == engine_url + '/user/create'
    assert create_user.query_parameters() == {}
    assert create_user.body_parameters() == {
        'profile': {
            'id': 'janedoe',
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'jane.doe@email.com'
        },
        'credentials': {
            'password': 'password'
        }
    }


@unittest.mock.patch('requests.post')
def test_create_calls_requests(mock, engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    create_user()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_create_raises_pycamunda_exception(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    with pytest.raises(pycamunda.PyCamundaException):
        create_user()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_create_raises_for_status(mock, engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    create_user()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_create_returns_none(engine_url, jane_doe_dict):
    create_user = pycamunda.user.Create(url=engine_url, **jane_doe_dict, password='password')
    result = create_user()

    assert result is None


def test_update_credentials_params(engine_url, update_credentials_input):
    update_credentials = pycamunda.user.UpdateCredentials(
        url=engine_url, **update_credentials_input
    )

    assert update_credentials.url == engine_url + '/user/janedoe/credentials'
    assert update_credentials.query_parameters() == {}
    assert update_credentials.body_parameters() == {
        'password': 'password',
        'authenticatedUserPassword': 'password'
    }


@unittest.mock.patch('requests.put')
def test_update_credentials_calls_requests(mock, engine_url, update_credentials_input):
    update_credentials = pycamunda.user.UpdateCredentials(
        url=engine_url, **update_credentials_input
    )
    update_credentials()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_update_credentials_raises_pycamunda_exception(engine_url, update_credentials_input):
    update_credentials = pycamunda.user.UpdateCredentials(
        url=engine_url, **update_credentials_input
    )
    with pytest.raises(pycamunda.PyCamundaException):
        update_credentials()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_credentials_raises_for_status(mock, engine_url, update_credentials_input):
    update_credentials = pycamunda.user.UpdateCredentials(
        url=engine_url, **update_credentials_input
    )
    update_credentials()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_update_credentials_returns_none(engine_url, update_credentials_input):
    update_credentials = pycamunda.user.UpdateCredentials(
        url=engine_url, **update_credentials_input
    )
    result = update_credentials()

    assert result is None


def test_update_profile_params(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)

    assert update_profile.url == engine_url + '/user/janedoe/profile'
    assert update_profile.query_parameters() == {}
    assert update_profile.body_parameters() == {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }


@unittest.mock.patch('requests.put')
def test_update_profile_calls_requests(mock, engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    update_profile()

    assert mock.called


@unittest.mock.patch('requests.put', raise_requests_exception_mock)
def test_update_profile_raises_pycamunda_exception(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)

    with pytest.raises(pycamunda.PyCamundaException):
        update_profile()


@unittest.mock.patch('requests.put', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_profile_raises_for_status(mock, engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    update_profile()

    assert mock.called


@unittest.mock.patch('requests.put', unittest.mock.MagicMock())
def test_update_profile_returns_none(engine_url, jane_doe_dict):
    update_profile = pycamunda.user.UpdateProfile(url=engine_url, **jane_doe_dict)
    result = update_profile()

    assert result is None


def test_unlock_user_params(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')

    assert unlock_user.url == engine_url + '/user/myuserid/unlock'
    assert unlock_user.query_parameters() == {}
    assert unlock_user.body_parameters() == {}


@unittest.mock.patch('requests.post')
def test_unlock_calls_requests(mock, engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    unlock_user()

    assert mock.called


@unittest.mock.patch('requests.post', raise_requests_exception_mock)
def test_unlock_raises_pycamunda_exception(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')

    with pytest.raises(pycamunda.PyCamundaException):
        unlock_user()


@unittest.mock.patch('requests.post', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_unlock_raises_for_status(mock, engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    unlock_user()

    assert mock.called


@unittest.mock.patch('requests.post', unittest.mock.MagicMock())
def test_unlock_returns_none(engine_url):
    unlock_user = pycamunda.user.Unlock(url=engine_url, id_='myuserid')
    result = unlock_user()

    assert result is None
