import asyncio
import gzip
import lzma
from contextlib import contextmanager
from unittest.mock import AsyncMock, Mock, patch

import pytest
from a8t_tools.storage.local_storage import LocalStorageBackend
from celery import Celery
from freezegun import freeze_time

import app.domain
from app.fastapi import fastapi_app
from tests import __root_dir__, utils


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def frozen_time():
    with freeze_time() as ft:
        with patch("asyncio.sleep", new_callable=AsyncMock):
            yield ft


@pytest.fixture(scope="session")
def client(event_loop):
    yield utils.TestClientSessionExpire(fastapi_app)


@pytest.fixture(scope="session")
def container(client):
    client.application.extra["container"].wire(packages=[app.domain])
    yield client.application.extra["container"]


@pytest.fixture()
def container_singletone(container):
    with patch("app.containers.Container", new=lambda: container):
        yield container


@pytest.fixture()
def celery_app_mock(container):
    mock = Mock(Celery)
    with container.celery_app.override(mock):
        yield mock


@pytest.fixture()
def local_storage_mock(container):
    mock = Mock(LocalStorageBackend)
    with container.local_storage_backend.override(mock):
        yield mock


@pytest.fixture()
def db_transaction():
    return fastapi_app.extra["container"].transaction()


@pytest.fixture()
def file_fixture():
    @contextmanager
    def wrapper(fixture_name):
        if fixture_name.endswith(".gz"):
            file_open = gzip.open
        if fixture_name.endswith(".lzma"):
            file_open = lzma.open
        else:
            file_open = open
        path = f"{__root_dir__}/fixtures/{fixture_name}"
        with file_open(path, "rt") as f:
            yield f

    return wrapper


@pytest.fixture()
def token_data_factory(container):
    async def wrapper(user):
        return await container.user.token_create_command()(user)

    return wrapper


@pytest.fixture()
def token_headers_factory(token_data_factory) -> str:
    async def wrapped(user) -> dict[str, str]:
        token_data = await token_data_factory(user=user)
        headers = dict(Authorization=f"Bearer {token_data.access_token}")
        return headers

    return wrapped
