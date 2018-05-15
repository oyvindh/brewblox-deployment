"""
Tests basic functionality of the history service
"""

import asyncio
import json

import pytest
from nesdict import NesDict as Nesdict


@pytest.fixture
def data():
    with open('test/MOCK_DATA.json') as f:
        data = json.load(f)
    return data


@pytest.mark.asyncio
async def test_publish_values(session, host, data):

    await session.post(host + '/history/subscribe', json={'exchange': 'brewblox', 'routing': 'controller1.#'})

    for d in data:
        await session.post(host + '/publisher/_debug/publish', json={
            'exchange': 'brewblox',
            'routing': 'controller1.dummy',
            'message': d
        })

    await asyncio.sleep(2)

    await session.post(host + '/history/_debug/query',
                       json={'database': 'brewblox', 'query': 'SHOW DATABASES'})

    res = await session.post(host + '/history/_debug/query',
                             json={'database': 'brewblox', 'query': 'SHOW MEASUREMENTS'})
    content = Nesdict(await res.json())
    assert content.get('results/0/series')

    res = await session.post(host + '/history/_debug/query',
                             json={'database': 'brewblox', 'query': 'SELECT * FROM controller1 LIMIT 100'})

    content = Nesdict(await res.json())
    assert content.get('results/0/series/0/values')
