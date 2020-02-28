# -*- coding: utf-8 -*-

"""This module provides access to the filter REST api of Camunda."""

import requests
import dataclasses
import typing

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/filter'


class Create(pycamunda.request.CamundaRequest):

    resource_type = BodyParameter('resourceType')
    name = BodyParameter('name')
    owner = BodyParameter('owner')
    query = BodyParameterContainer('query')
    properties = BodyParameterContainer('properties')

    def __init__(self, url, resource_type=None, name=None, owner=None):
        """Create a new filter.

        :param url: Camunda Rest engine URL.
        :param resource_type: Resource type of the filter.
        :param name: Name of the filter.
        :param owner: User id of the owner of the filter.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.resource_type = resource_type
        self.name = name
        self.owner = owner

    def add_query(self, **kwargs):
        for key, value in kwargs.items():
            self.query.parameters[key] = value

    def add_properties(self, **kwargs):
        for key, value in kwargs.items():
            self.properties.parameters[key] = value

    def send(self):
        """Send the request"""
        params = self.body_parameters()
        try:
            response = requests.post(self.url, json=params)
        except requests.exceptions.RequestException as exc:
            raise pycamunda.PyCamundaException(exc)
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)
