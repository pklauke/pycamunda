# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def engine_url():
    return 'http://localhost/engine-rest'
