# -*- coding: utf-8 -*-

"""This module provides access to the case definition REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses


@dataclasses.dataclass
class CaseDefinition:
    """Data class of case definition as returned by the REST api of Camunda."""
    id_: str
    key: str
    category: str
    name: str
    version: int
    resource: str
    deployment_id: str
    tenant_id: str
    history_time_to_live: int

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> CaseDefinition:
        return cls(
            id_=data['id'],
            key=data['key'],
            category=data['category'],
            name=data['name'],
            version=data['version'],
            resource=data['resource'],
            deployment_id=data['deploymentId'],
            tenant_id=data['tenantId'],
            history_time_to_live=data['historyTimeToLive']
        )
