import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.main import get_app
from app.db import dispose_engine


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # <-- важно!
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    return get_app()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def shutdown_engine():
    yield
    await dispose_engine()
