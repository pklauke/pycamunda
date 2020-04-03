# -*- coding: utf-8 -*-
from __future__ import annotations
import dataclasses
import typing


class PyCamundaException(Exception):
    """Base class for all PyCamunda exceptions."""


class PyCamundaNoSuccess(PyCamundaException):
    """Exception that is raised when a request is not successful."""

class PyCamundaInvalidInput(PyCamundaNoSuccess):
    """Exception that is raised when invalid input is given to a request."""


class PyCamundaUserAlreadyExists(PyCamundaNoSuccess):
    """Exception that is raised when it is tried to create a user that already exists."""


@dataclasses.dataclass
class Link:
    method: str
    href: str
    rel: str

    @classmethod
    def load(cls, data) -> Link:
        return Link(
            method=data['method'],
            href=data['href'],
            rel=data['rel'],
        )


@dataclasses.dataclass
class ResourceOptions:
    links: typing.Tuple[Link]

    def __iter__(self):
        return (link for link in self.links)

    def __len__(self):
        return len(self.links)

    @classmethod
    def load(cls, data) -> ResourceOptions:
        return ResourceOptions(
            links=tuple(Link(**link) for link in data['links'])
        )
