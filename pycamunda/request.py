# -*- coding: utf-8 -*-

import abc
import collections
from typing import Mapping, Callable


class RequestParameter:

    def __init__(self, key, mapping: Mapping=None, provide: Callable=None):
        """Parameter that is send with a CamundaRequest when it is attached to the class and its value is set. This
        class implements the descriptor protocol.

        :param key: Camunda key of the request parameter.
        """
        self.key = key
        self.mapping = mapping
        self.provide = provide
        self.name = None

    def __get__(self, obj, obj_type=None):
        if self.provide is None or self.provide(self):
            if self.mapping is None:
                return obj.__dict__[self.name]
            return self.mapping[obj.__dict__[self.name]]

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __repr__(self):
        return f'{self.__class__.__name__}(key={self.key})'


class QueryParameter(RequestParameter):
    """Parameter that is attached to the request URL by adding it after the endpoint name."""


class PathParameter(RequestParameter):
    """Parameter that is attached to the request URL by adding it to the endpoint name."""


class BodyParameter(RequestParameter):
    """Parameter that is attached to the request body."""


class BodyParameterContainer:
    """Stores multiple BodyParameters`s and allows sending nested queries.

    :param key: Camunda key.
    :param args: BodyParameter`s
    """
    def __init__(self, key, *args):
        self.key = key
        self.parameters = {}
        for arg in args:
            self.parameters[arg.key] = arg

    def __repr__(self):
        return f'{self.__class__.__qualname__}(key={self.key}, ' \
               f'{", ".join(k+"="+str(v) for k, v in self.parameters.items())})'


class CamundaRequestMeta(abc.ABCMeta):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, RequestParameter):
                attr.name = key


class CamundaRequest(metaclass=CamundaRequestMeta):

    def __init__(self, url):
        """Abstract base class for Camunda requests. Extracts parameters to send with the requests by parsing the class
            for RequestParameter`s.

        :param url: Camunda Rest engine url.
        """
        self._url = url

    @property
    def url(self):
        params = {}
        missing_params = {}
        for name, attribute in vars(type(self)).items():
            if isinstance(attribute, PathParameter):
                try:
                    params[attribute.key] = getattr(self, attribute.name)
                except KeyError:
                    missing_params[attribute.key] = ''
        return self._url.format(**{**params, **missing_params}).rstrip('/')

    def __call__(self, *args, **kwargs):
        return self.send()

    @abc.abstractmethod
    def send(self):
        return NotImplemented

    def query_parameters(self):
        query = {}
        for name, attribute in vars(type(self)).items():
            if isinstance(attribute, QueryParameter):
                try:
                    query[attribute.key] = getattr(self, attribute.name)
                except KeyError:
                    pass
        return query

    def _traverse(self, container):
        query = {}
        for key, val in container.parameters.items():
            if isinstance(val, BodyParameterContainer):
                query[key] = self._traverse(val)
            else:
                try:
                    value = getattr(self, val.name)
                except KeyError:
                    pass
                except AttributeError:
                    if val is not None:
                        query[key] = val
                else:
                    if value is not None:
                        query[key] = value
        return query

    def body_parameters(self):
        query = {}
        parameters = []
        for name, attribute in vars(type(self)).items():
            if isinstance(attribute, BodyParameterContainer):
                query[attribute.key] = self._traverse(attribute)
                parameters += list(attribute.parameters)
        parameters = set(parameters)
        for name, attribute in vars(type(self)).items():
            if isinstance(attribute, BodyParameter) and attribute.key not in parameters:
                try:
                    value = getattr(self, attribute.name)
                except KeyError:
                    pass
                else:
                    if value is not None:
                        query[attribute.key] = value
        return query
