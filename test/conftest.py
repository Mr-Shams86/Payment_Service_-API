import os
import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

# from app.main import get_app
# from app.db import dispose_engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # <-- важно!
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    os.environ["ENV"] = "test"
    os.environ["DB_HOST"] = "127.0.0.1"
    os.environ["DB_PORT"] = "5434"

    from app.main import get_app
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
    from app.db import dispose_engine
    await dispose_engine()
