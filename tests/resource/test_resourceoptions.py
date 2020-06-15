# -*- coding: utf-8 -*-

import pytest

import pycamunda.resource


def test_resourceoptions_load(my_link_json):
    resource_options = pycamunda.resource.ResourceOptions.load({'links': [my_link_json] * 2})

    assert isinstance(resource_options.links, tuple)
    assert all(isinstance(link, pycamunda.resource.Link) for link in resource_options)
    assert len(resource_options) == 2


def test_link_load_raises_keyerror(my_link_json):
    with pytest.raises(KeyError):
        pycamunda.resource.Link.load({})
