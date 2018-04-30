import asyncio
import logging

import aiohttp
import pytest
from async_timeout import timeout
from itertools import chain

from subprocess import call, STDOUT


@pytest.fixture(scope='session', autouse=True)
def log_enabled():
    """Sets log level to DEBUG for all test functions.
    Allows all logged messages to be captured during pytest runs"""
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)


@pytest.yield_fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def host():
    return 'http://127.0.0.1'


@pytest.fixture(scope='session')
def services():
    return [
        'history',
        'publisher'
    ]


@pytest.fixture(scope='session', autouse=True)
def compose(services, log_enabled):

    try:
        call('docker-compose up --force-recreate --no-color --remove-orphans -d'.split())
        yield
    finally:
        # Sequentially logs from all brewblox services to file
        for svc in services:
            with open(f'logs/{svc}_service_log.txt', 'w') as f:
                call(f'docker-compose logs --no-color {svc}'.split(), stdout=f, stderr=STDOUT)

        with open('logs/compose_ps_log.txt', 'w') as f:
            call('docker-compose ps'.split(), stdout=f, stderr=STDOUT)

        call('docker-compose down'.split())


@pytest.fixture(scope='session')
async def session(event_loop, services, host):

    # Helper function: make http calls to heartbeat / ping endpoints until they're ok
    async def wait_online(session, addr):
        while True:
            try:
                res = await session.get(addr)
                assert res.status < 400
                break
            except Exception:
                await asyncio.sleep(0.1)

    # Create session. This will be used for all tests
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with timeout(15):
            await asyncio.wait(
                chain(
                    [wait_online(session, f'{host}/{svc}/_service/status') for svc in services],
                    [
                        wait_online(session, host + ':15672/'),  # eventbus management port
                        wait_online(session, host + ':8086/ping'),  # influxdb status check
                    ]
                )
            )

        yield session
