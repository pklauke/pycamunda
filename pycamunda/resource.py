# -*- coding: utf-8 -*-

"""This module provides access to the resource REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing
import enum


__all__ = ['ResourceType']


@dataclasses.dataclass
class Link:
    """Data class of link as returned by the REST api of Camunda."""
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
    """Data class of resource options as returned by the REST api of Camunda."""
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


class ResourceType(enum.IntEnum):
    application = 0
    user = 1
    group = 2
    group_membership = 3
    authorization = 4
    filter_ = 5
    process_definition = 6
    task = 7
    process_instance = 8
    deployment = 9
    decision_definition = 10
    tenant = 11
    tenant_membership = 12
    batch = 13
    decision_requirements_definition = 14
    report = 15
    dashboard = 16
    user_operation_log_category = 17
    optimize = 18
    historic_task = 19
    historic_process_instance = 20
