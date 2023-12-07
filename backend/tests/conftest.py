import asyncio
from typing import Generator, Any

from elasticsearch import AsyncElasticsearch
from tests.test_data import products
import settings
from db.elasticsearch.indexes import NAME_INDEX_PRODUCTS
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

@pytest.fixture(scope="function")
async def create_products():
    test_elastic_client = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    for test_product in products:
        await test_elastic_client.index(index=NAME_INDEX_PRODUCTS, document=test_product)
    return products

@pytest.fixture(scope="function", autouse=True)
async def clean_index():
    test_elastic_client = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    await test_elastic_client.delete_by_query(index=NAME_INDEX_PRODUCTS, query={"match_all": {}}, params={"refresh": "true"})
