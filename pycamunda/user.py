# -*- coding: utf-8 -*-

"""This module provides access to the user REST api of Camunda."""

import requests

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/user'


class Delete(pycamunda.request.CamundaRequest):

    user_id = PathParameter('id')

    def __init__(self, url):
        """Deletes a user by id.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.user_id = None

    def send(self):
        """Send the request"""
        try:
            response = requests.delete(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class Count(pycamunda.request.CamundaRequest):

    user_id = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')

    def __init__(self, url):
        """Deletes a user by id.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/count')

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

    user_id = QueryParameter('id')
    first_name = QueryParameter('firstName')
    first_name_like = QueryParameter('firstNameLike')
    last_name = QueryParameter('lastName')
    last_name_like = QueryParameter('lastNameLike')
    email = QueryParameter('email')
    email_like = QueryParameter('emailLike')
    member_of_group = QueryParameter('memberOfGroup')
    member_of_tenant = QueryParameter('memberOfTenant')
    sort_by = QueryParameter('sortBy')
    sort_order = QueryParameter('sortOrder')
    first_result = QueryParameter('firstResult')
    max_results = QueryParameter('maxResults')

    def __init__(self, url):
        """Query for a list of users using a list of parameters. The size of the result set can be
        retrieved by using the Get User Count method.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX)

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

    user_id = PathParameter('id')

    def __init__(self, url):
        """

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')

    def send(self):
        """Send the request"""
        print(self.url)
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return response.json()


class Options(pycamunda.request.CamundaRequest):

    user_id = PathParameter('id')

    def __init__(self, url):
        """Query for a list of users using a list of parameters. The size of the result set can be
        retrieved by using the Get User Count method.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')

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

    user_id = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')
    profile = BodyParameterContainer('profile', user_id, first_name, last_name, email)

    password = BodyParameter('password')
    credentials = BodyParameterContainer('credentials', password)

    def __init__(self, url):
        """Create a new user.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')

    def send(self):
        """Send the request"""
        query = self.body_parameters()
        try:
            response = requests.post(self.url, json=query)
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

    user_id = PathParameter('id')
    password = BodyParameter('password')
    authenticated_user_password = BodyParameter('authenticatedUserPassword')

    def __init__(self, url):
        """Updates a user's credentials (password).

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/credentials')

    def send(self):
        """Send the request"""
        query = self.body_parameters()
        try:
            response = requests.put(self.url, json=query)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)


class UpdateProfile(pycamunda.request.CamundaRequest):

    user_id = PathParameter('id')
    new_user_id = BodyParameter('id')
    first_name = BodyParameter('firstName')
    last_name = BodyParameter('lastName')
    email = BodyParameter('email')

    def __init__(self, url):
        """Updates the profile information of an already existing user.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}/profile')

    def send(self):
        """Send the request"""
        query = self.body_parameters()
        try:
            response = requests.put(self.url, json=query)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)
