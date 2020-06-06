# -*- coding: utf-8 -*-
from __future__ import annotations


class PyCamundaException(Exception):
    """Base class for all PyCamunda exceptions."""


class NoSuccess(PyCamundaException):
    """Exception that is raised when the tried action is not successful."""
    http_code = None


class BadRequest(NoSuccess):
    """Exception that is raised when the tried action was invalid."""
    http_code = 400


class Forbidden(NoSuccess):
    """Exception that is raised when the tried action was valid but not permitted."""
    http_code = 403


class NotFound(NoSuccess):
    """Exception that is raised when the requested resource was not found."""
    http_code = 404


class InternalServerError(PyCamundaException):
    """Exception that is raised when there occurred an error on Camunda server side."""
    http_code = 500
