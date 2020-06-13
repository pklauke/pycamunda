# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def my_link_json():
    return {
        'method': 'GET',
        'href': 'http://localhost/',
        'rel': 'self'
    }
