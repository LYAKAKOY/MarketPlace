import asyncio
from typing import Generator, Any
from db.elasticsearch.session import get_db_es
import pytest
from httpx import AsyncClient

from main import app
from tests.db_es_test import get_test_db_es

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `get_db` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db_es] = get_test_db_es
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client
