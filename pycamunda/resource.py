# -*- coding: utf-8 -*-

"""This module provides access to the resource REST api of Camunda."""

from __future__ import annotations
import dataclasses
import typing


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
