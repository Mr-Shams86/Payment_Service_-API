import sys
import pytest

from pathlib import Path

from httpx import AsyncClient, ASGITransport

from app.main import get_app


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session")
def app():
    return get_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client
