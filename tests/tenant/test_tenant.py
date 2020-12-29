# -*- coding: utf-8 -*-

import pytest

import pycamunda.base
import pycamunda.tenant
import pycamunda.resource


def test_tenant_load():
    tenant = pycamunda.tenant.Tenant.load(data={'id': 'aTenant', 'name': 'a tenant'})

    assert isinstance(tenant, pycamunda.tenant.Tenant)
    assert tenant.id_ == 'aTenant'
    assert tenant.name == 'a tenant'


def test_tenant_load_raises_key_error():
    with pytest.raises(KeyError):
        pycamunda.tenant.Tenant.load(data={'name': 'a tenant'})
    with pytest.raises(KeyError):
        pycamunda.tenant.Tenant.load(data={'id': 'aTenant'})
