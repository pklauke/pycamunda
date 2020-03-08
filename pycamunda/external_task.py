# -*- coding: utf-8 -*-

"""This module provides access to the external task REST api of Camunda."""

import dataclasses

import requests

import pycamunda
import pycamunda.request
from pycamunda.request import PathParameter, QueryParameter, BodyParameter, BodyParameterContainer


URL_SUFFIX = '/external-task'


@dataclasses.dataclass
class ExternalTask:
    activity_id: str
    activity_instance_id: str
    error_message: str
    error_details: str
    execution_id: str
    id_: str
    lock_expiration_time: str
    process_definition_id: str
    process_definition_key: str
    process_instance_id: str
    tenant_id: str
    retries: int
    suspended: bool
    worker_id: str
    priority: str
    topic_name: str

    @classmethod
    def load(cls, data):
        return ExternalTask(
            activity_id=data['activityId'],
            activity_instance_id=data['activityInstanceId'],
            error_message=data['errorMessage'],
            error_details=data['errorDetails'],
            execution_id=data['executionId'],
            id_=data['id'],
            lock_expiration_time=data['lockExpirationTime'],
            process_definition_id=data['processDefinitionId'],
            process_definition_key=data['processDefinitionKey'],
            process_instance_id=data['processInstanceId'],
            tenant_id=data['tenantId'],
            retries=data['retries'],
            suspended=data['suspended'],
            worker_id=data['workerId'],
            priority=data['priority'],
            topic_name=data['topicName']
        )


class Get(pycamunda.request.CamundaRequest):

    id_ = PathParameter('id')

    def __init__(self, url, id_):
        """Query for an external task.

        :param url: Camunda Rest engine URL.
        :param id_: Id of the external task.
        """
        super().__init__(url=url + URL_SUFFIX + '/{id}')
        self.id_ = id_

    def send(self):
        """Send the request"""
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            raise pycamunda.PyCamundaException()
        if not response:
            raise pycamunda.PyCamundaNoSuccess(response.text)

        return ExternalTask.load(response.json())

