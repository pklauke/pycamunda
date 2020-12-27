# -*- coding: utf-8 -*-

"""This module provides access to the tenant REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing

import pycamunda
import pycamunda.base
from pycamunda.request import QueryParameter, PathParameter, BodyParameter, BodyParameterContainer

URL_SUFFIX = '/tenant'


__all__ = ['Get', 'Create']


@dataclasses.dataclass
class Tenant:
    """Data class of tenant as returned by the REST api of Camunda."""
    id_: str
    name: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> Tenant:
        return cls(id_=data['id'], name=data['name'])


class Get(pycamunda.base.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url: str, id_: str):
        """Get a tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def __call__(self, *args, **kwargs) -> Tenant:
        """Send the request"""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return Tenant.load(response.json())


class Create(pycamunda.base.CamundaRequest):

    id_ = BodyParameter('id')
    name = BodyParameter('name')

    def __init__(self, url: str, id_: str, name: str):
        """Create a new tenant.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the tenant.
        :param name: Name of the tenant.
        """
        super().__init__(url=url + URL_SUFFIX + '/create')
        self.id_ = id_
        self.name = name

    def __call__(self, *args, **kwargs) -> None:
        """Send the request"""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)
