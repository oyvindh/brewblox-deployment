"""
Tests the brewblox-devcon-spark service
"""
import asyncio
import json

import pytest
from aiohttp.client_exceptions import ClientResponseError


@pytest.fixture
def sensey():
    return {
        'id': 'sensey',
        'profiles': [0, 3, 7],
        'type': 'TempSensorOneWire',
        'data': {
            'address': 'FF',
            'offset[delta_degF]': 20
        }
    }


async def response(coro):
    retv = await coro
    return await retv.json()


def ids(obj_list):
    return {obj['id'] for obj in obj_list}


@pytest.mark.asyncio
async def test_profiles(session, host):
    url = host + '/spark/system/profiles'
    assert await response(session.get(url)) == [0]

    all_profiles = [i for i in range(8)]
    assert await response(session.put(url, json=all_profiles)) == all_profiles
    assert await response(session.get(url)) == all_profiles


@pytest.mark.asyncio
async def test_units(session, host):
    units = {
        'Temp': 'degC',
        'Time': 'second',
        'LongTime': 'hour',
    }
    assert await response(session.put(host + '/spark/codec/units', json=units)) == units
    assert await response(session.put(host + '/sparktwo/codec/units', json=units)) == units


@pytest.mark.asyncio
async def test_create_objects(session, host, sensey):
    create_url = host + '/spark/objects'
    retd = await response(session.post(create_url, json=sensey))
    print(retd)

    assert retd['id'] == sensey['id']
    assert retd['data']['offset[delta_degC]']

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
    assert retd['data']['offset[delta_degC]']

    await session.get(host + '/spark/objects/sensex')


@pytest.mark.asyncio
async def test_read_all(session, host):
    retd = await response(session.get(host + '/spark/objects'))

    assert {'sensey', 'sensex'}.issubset(ids(retd))
    assert retd[-1]['id'] == 'sensex'
    assert retd[-1]['type'] == 'TempSensorOneWire'


@pytest.mark.asyncio
async def test_reset_objects(session, host):
    with open('seed_objects.json') as f:
        objs = json.load(f)

    await response(session.post(host + '/sparktwo/reset_objects', json=objs))
    retd = await response(session.get(host + '/sparktwo/objects'))

    assert {'setpoint-1', 'setpoint-2', 'setpoint-inactive', 'sensor-1', 'sensor-onewire-1',
            'setpoint-sensor-pair-1', 'actuator-1', 'actuator-pwm-1', 'pid-1'}.issubset(ids(retd))


@pytest.mark.asyncio
async def test_read_active(session, host):
    await session.put(host + '/spark/system/profiles', json=[])
    retd = await response(session.get(host + '/spark/objects'))
    assert retd[-1]['id'] == 'sensex'
    assert retd[-1]['type'] == 'InactiveObject'

    # activate some empty profiles
    await session.put(host + '/spark/system/profiles', json=[1, 2])
    retd = await response(session.get(host + '/spark/objects'))
    assert retd[-1]['id'] == 'sensex'
    assert retd[-1]['type'] == 'InactiveObject'

    # activate filled profiles
    await session.put(host + '/spark/system/profiles', json=[0, 3, 7])
    retd = await response(session.get(host + '/spark/objects'))
    assert retd[-1]['id'] == 'sensex'
    assert retd[-1]['type'] == 'TempSensorOneWire'

    # all objects are active now
    stored = await response(session.get(host + '/spark/stored_objects'))
    assert 'InactiveObject' not in {obj['type'] for obj in stored}


@pytest.mark.asyncio
async def test_write_object(session, host, sensey):
    url = host + '/spark/objects/sensey'
    del sensey['id']
    sensey['data']['offset[delta_degF]'] = 30

    await session.put(url, json=sensey)
    retd = await response(session.get(url))
    assert retd['data']['offset[delta_degC]'] == pytest.approx(16.7, 0.1)


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
async def test_add_remote_block(session, host, sensey):
    sensey['id'] = 'remoteblock'

    await response(session.post(host + '/spark/objects', json=sensey))
    await response(session.post(host + '/sparktwo/objects', json=sensey))

    key = await response(session.post(host + '/spark/remote/master', json={
        'id': 'remoteblock',
        'interval': 1
    }))
    assert key['key']

    await response(session.post(host + '/sparktwo/remote/slave', json={
        'id': 'remoteblock',
        'key': key['key'],
        'translations': {'offset[delta_degC]': 'value[degC]'}
    }))

    sensey['data']['offset[delta_degF]'] = 30
    await response(session.put(host + '/spark/objects/remoteblock', json=sensey))


@pytest.mark.asyncio
async def test_sleepytime():
    # Data is broadcasted every set interval
    # We've started the broadcasts previously, now wait to ensure something is sent
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_broadcast(session, host):
    retd = await response(session.post(host + '/history/query/objects', json={}))
    print(retd)
    assert 'setpoint-1/setting[degC]' in retd['sparktwo']

    retd = await response(session.post(host + '/history/query/values', json={
        'measurement': 'sparktwo'
    }))
    print(retd)
    assert 'setpoint-1/setting[degC]' in retd['columns']


@pytest.mark.asyncio
async def test_remote_updated(session, host):
    vals = await response(session.get(host + '/sparktwo/objects/remoteblock'))
    print(vals)

    # We set master block offset to 30F, and translated offset to value in slave block
    # We expect slave offset to be default setting (20 delta_degF to delta_degC),
    # and the value to match master offet (30 delta_degF to degC)
    # Note that no unit conversions are done when translating
    assert vals['data']['offset[delta_degC]'] == pytest.approx(11.1, abs=0.1)
