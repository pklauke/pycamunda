# -*- coding: utf-8 -*-

"""This module provides access to the user REST api of Camunda."""

import requests

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/user'


class Delete(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """Deletes a user by id.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class Count(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')

    def __init__(self, url, id_=None):
        """Count users.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')
        self.id_ = id_

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()['count']


class Get(pycamunda.request.CamundaRequest):

    id_ = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')
    sort_by = QueryParameter('sortBy')
    ascending = QueryParameter('sortOrder', mapping={True: 'asc', False: 'desc'},
                               provide=lambda self: 'sort_by' in vars(self))
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url, id_=None, first_name=None, first_name_like=None, last_name=None,
                 last_name_like=None, email=None, email_like=None, member_of_group=None,
                 member_of_tenant=None, sort_by=None, ascending=True, first_result=None,
                 max_results=None):
        """Query for a list of users using a list of parameters. The size of the result set can be
        retrieved by using the Get User Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param first_name: Filter by the first name of the user.
        :param first_name_like: Filter by a substring of the first name.
        :param last_name: Filter by the last name of the user.
        :param last_name_like: Filter by a substring of the last name.
        :param email: Filter by the email of the user.
        :param email_like: Filter by a substring of the email.
        :param member_of_group: Filter for users which are a member of a group.
        :param member_of_tenant: Filter for users which are a member of a tenant.
        :param sort_by: Sort the results by `id`, `first_name`, `last_name` or `email` of the user.
        :param ascending: Sort order.
        :param first_result: Pagination of results. Index of the first result to return.
        :param max_results: Pagination of results. Maximum number of results to return.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.id_ = id_
        self.first_name = first_name
        self.first_name_like = first_name_like
        self.last_name = last_name
        self.last_name_like = last_name_like
        self.email = email
        self.email_like = email_like
        self.member_of_group = member_of_group
        self.member_of_tenant = member_of_tenant
        self.sort_by = sort_by
        self.ascending = ascending
        self.first_result = first_result
        self.max_results = max_results

    def send(self):
        """Send the request"""
        params = self.query_parameters()
        try:
            response = requests.get(self.url, params=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()


class GetProfile(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()


class Options(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_=None):
        """Query for a list of users using a list of parameters. The size of the result set can be
        retrieved by using the Get User Count method.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.options(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()


class Create(pycamunda.request.CamundaRequest):

    id_ = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')
    profile = BodyParameterContainer('profile', id_, first_name, last_name, email)

    password = BodyParameter('password')
    credentials = BodyParameterContainer('credentials', password)

    def __init__(self, url, id_=None, first_name=None, last_name=None, email=None, password=None):
        """Create a new user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param email: Email of the user.
        :param password: Password of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            try:
                if response.json()['message'] == "The user already exists":
                    raise pycamunda.PyCamundaUserAlreadyExists(response.text)
            except KeyError:
                pass
            raise pycamunda.PyCamundaNoSuccess(response.text)


class UpdateCredentials(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    password = BodyParameter('password')
    authenticated_user_password = BodyParameter('authenticatedUserPassword')

    def __init__(self, url, id_, password, authenticated_user_password):
        """Updates a user's credentials (password).

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param password: New password of the user.
        :param authenticated_user_password: Password of the authenticated user who changes the
                                            password.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/credentials')
        self.id_ = id_
        self.password = password
        self.authenticated_user_password = authenticated_user_password

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class UpdateProfile(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')
    new_user_id = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')

    def __init__(self, url, id_, new_user_id=None, first_name=None, last_name=None, email=None):
        """Updates the profile information of an already existing user.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the user.
        :param new_user_id: New user id of the user.
        :param first_name: New first name of the user.
        :param last_name: New last name of the user.
        :param email: New email of the user.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')
        self.id_ = id_
        self.new_user_id = new_user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.put(self.url, json=params)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)
