# -*- coding: utf-8 -*-
import requests


def raise_requests_exception_mock(*args, **kwargs):
    raise requests.exceptions.RequestException


def not_ok_response_mock(*args, **kwargs):
    class Response:
        ok = False
        text = ''

        def __bool__(self):
            return bool(self.ok)

        def json(self):
            return {'message': 'an error message'}

    return Response()


def count_response_mock(*args, **kwargs):
    class Response:
        ok = True

        def __bool__(self):
            return bool(self.ok)

        def json(self):
            return {'count': 1}

    return Response()