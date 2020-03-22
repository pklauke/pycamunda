# -*- coding: utf-8 -*-

from __future__ import annotations
import dataclasses
import enum


class IncidentType(enum.Enum):
    failed_job = 'failedJob'
    failed_external_task = 'failedExternalTask'


@dataclasses.dataclass
class Incident:
    incident_type: IncidentType
    incident_count: int

    @classmethod
    def load(cls, data) -> Incident:
        return cls(
            incident_type=IncidentType(data['incidentType']),
            incident_count=data['incidentCount']
        )
