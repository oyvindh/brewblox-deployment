"""
Tests basic features of connected services
"""


import asyncio

import pytest


@pytest.mark.asyncio
async def test_brewblox_generics(session, host, services):
    """We expect all brewblox services to offer these endpoints"""
    for f in asyncio.as_completed(
        [
            session.get(f'{host}/{svc}/{endpoint}')
            for svc in services
            for endpoint in [
                '_service/status',
                'api/doc'
            ]
        ]
    ):
        res = await f
        assert res.status == 200
