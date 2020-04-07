# -*- coding: utf-8 -*-

from __future__ import annotations
import dataclasses
import typing


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
