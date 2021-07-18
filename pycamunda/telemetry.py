# -*- coding: utf-8 -*-

"""This module provides access to the telemetry REST api of Camunda."""

from __future__ import annotations

import pycamunda
import pycamunda.base
import pycamunda.resource
from pycamunda.request import BodyParameter

URL_SUFFIX = '/telemetry/configuration'


__all__ = ['Configure', 'Fetch']


class Configure(pycamunda.base.CamundaRequest):

    enable_telemetry = BodyParameter('enableTelemetry')

    def __init__(self, url: str, enable_telemetry: bool):
        """Modify the telemetry configuration.

        :param url: Camunda Rest engine URL.
        :param enable_telemetry: Whether to enable telemetry configuration.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.enable_telemetry = enable_telemetry

    def __call__(self, *args, **kwargs) -> None:
        """Send the request."""
        super().__call__(pycamunda.base.RequestMethod.POST, *args, **kwargs)


class Fetch(pycamunda.base.CamundaRequest):

    def __init__(self, url: str):
        """Fetch the telemetry configuration.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX)

    def __call__(self, *args, **kwargs) -> bool:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)

        return response.json()['enableTelemetry']
