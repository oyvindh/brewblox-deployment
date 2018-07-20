"""
Tests the brewblox-devcon-spark service
"""
import asyncio

import pytest
from aiohttp.client_exceptions import ClientResponseError


@pytest.fixture
def sensey():
    return {
        'id': 'sensey',
        'profiles': [0, 3, 7],
        'type': 'OneWireTempSensor',
        'data': {
            'settings': {
                'address': 'FF',
                'offset[delta_degF]': 20
            }
        }
    }


async def response(coro):
    retv = await coro
    return await retv.json()


@pytest.mark.asyncio
async def test_profiles(session, host):
    url = host + '/spark/profiles'
    assert await response(session.get(url)) == []

    all_profiles = [i for i in range(8)]
    assert await response(session.post(url, json=all_profiles)) == all_profiles
    assert await response(session.get(url)) == all_profiles


@pytest.mark.asyncio
async def test_create_objects(session, host, sensey):
    create_url = host + '/spark/objects'
    retd = await response(session.post(create_url, json=sensey))
    print(retd)

    assert retd['id'] == sensey['id']
    assert retd['data']['settings']['offset[delta_degC]']

    sensey['id'] = 'sensex'
    await session.post(create_url, json=sensey)

    with pytest.raises(ClientResponseError):
        del sensey['id']
        await session.post(create_url, json=sensey)


@pytest.mark.asyncio
async def test_read_objects(session, host, sensey):
    retd = await response(session.get(host + '/spark/objects/sensey'))
    print(retd)

    assert retd['id'] == 'sensey'
    assert retd['data']['settings']['offset[delta_degC]']

    await session.get(host + '/spark/objects/sensex')


@pytest.mark.asyncio
async def test_read_all(session, host):
    retd = await response(session.get(host + '/spark/saved_objects'))

    assert len(retd) == 2
    assert retd[0]['id'] == 'sensey'
    assert retd[1]['id'] == 'sensex'

    assert retd[0]['type'] == 'OneWireTempSensor'


@pytest.mark.asyncio
async def test_read_active(session, host):
    await session.post(host + '/spark/profiles', json=[])
    retd = await response(session.get(host + '/spark/objects'))
    assert len(retd) == 0

    # activate some empty profiles
    await session.post(host + '/spark/profiles', json=[1, 2])
    retd = await response(session.get(host + '/spark/objects'))
    assert len(retd) == 0

    # activate filled profiles
    await session.post(host + '/spark/profiles', json=[0, 3, 7])
    retd = await response(session.get(host + '/spark/objects'))
    assert len(retd) == 2

    # all objects are active now
    assert retd == await response(session.get(host + '/spark/saved_objects'))


@pytest.mark.asyncio
async def test_write_object(session, host, sensey):
    url = host + '/spark/objects/sensey'
    del sensey['id']
    sensey['data']['settings']['offset[delta_degF]'] = 30

    await session.put(url, json=sensey)
    retd = await response(session.get(url))
    assert retd['data']['settings']['offset[delta_degC]'] == pytest.approx(16.7, 0.1)


@pytest.mark.asyncio
async def test_delete_object(session, host, sensey):
    url = host + '/spark/objects'
    sensey['id'] = 'sensey_del'

    await session.post(url, json=sensey)
    await session.get(url + '/sensey_del')
    await session.delete(url + '/sensey_del')

    with pytest.raises(ClientResponseError):
        await session.get(url + '/sensey_del')


@pytest.mark.asyncio
async def test_read_system(session, host):
    retd = await response(session.get(host + '/spark/system/onewirebus'))
    print(retd)
    assert retd['data']['address']


@pytest.mark.asyncio
async def test_write_system(session, host):
    retd = await response(session.get(host + '/spark/system/onewirebus'))
    print(retd)

    retd['data']['address'].append('cc')
    await session.put(host + '/spark/system/onewirebus', json=retd)

    retd = await response(session.get(host + '/spark/system/onewirebus'))
    print(retd)

    assert 'cc' in retd['data']['address']


@pytest.mark.asyncio
async def test_broadcast(session, host):
    # Sleep to ensure broadcaster has sent something
    await asyncio.sleep(2)

    retd = await response(session.post(host + '/history/query/objects', json={}))
    print(retd)
    assert 'sensey/settings/offset[delta_degC]' in retd['spark']

    retd = await response(session.post(host + '/history/query/values', json={
        'measurement': 'spark'
    }))
    print(retd)
    assert 'sensey/settings/offset[delta_degC]' in retd['columns']
