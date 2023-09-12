# -*- coding: utf-8 -*-

"""This module provides access to the version REST api of Camunda"""

from __future__ import annotations

import pycamunda.base

URL_SUFFIX = '/version'


__all__ = ['Get']


class Get(pycamunda.base.CamundaRequest):

    def __init__(self, url: str, timeout: int = 5):
        """Retrieve the version of the Rest api.

        :param url: Camunda Rest engine URL.
        """
        super().__init__(url=url + URL_SUFFIX)
        self.timeout = timeout

    def __call__(self, *args, **kwargs) -> str:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs, timeout=self.timeout)

        return response.json()['version']
