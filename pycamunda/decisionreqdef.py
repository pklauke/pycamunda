# -*- coding: utf-8 -*-

"""This module provides access to the decision requirements definition REST api of Camunda."""

from __future__ import annotations
import typing
import dataclasses


__all__ = []


@dataclasses.dataclass
class DecisionRequirementsDefinition:
    """Data class of decision requirements definition as returned by the REST api of Camunda."""
    id_: str
    key: str
    category: str
    name: str
    version: int
    resource: str
    deployment_id: str
    tenant_id: str

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> DecisionRequirementsDefinition:
        return cls(
            id_=data['id'],
            key=data['key'],
            category=data['category'],
            name=data['name'],
            version=data['version'],
            resource=data['resource'],
            deployment_id=data['deploymentId'],
            tenant_id=data['tenantId']
        )
