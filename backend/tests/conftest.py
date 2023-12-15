import asyncio
import os
from typing import Any
from typing import Generator

import pytest
import settings
from db.elasticsearch.indexes import NAME_INDEX_PRODUCTS
from db.elasticsearch.session import get_db_es
from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from main import app
from tests.db_es_test import get_test_db_es


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    os.system("python db/elasticsearch/migrations.py")


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
async def test_async_client_es():
    test_async_client_es = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    yield test_async_client_es
    await test_async_client_es.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_index(test_async_client_es):
    await test_async_client_es.delete_by_query(
        index=NAME_INDEX_PRODUCTS, query={"match_all": {}}, refresh=True
    )


@pytest.fixture(scope="function")
async def create_products(test_async_client_es):
    for product in products_data:
        await test_async_client_es.index(
            index=NAME_INDEX_PRODUCTS, document=product, refresh=True
        )


async def create_product(document: dict):
    test_async_client_es = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    await test_async_client_es.index(
        index=NAME_INDEX_PRODUCTS, document=document, refresh=True
    )
    await test_async_client_es.close()


products_data = [
    {
        "id_company": 1,
        "product_name": "Product A",
        "description": "Description A H",
        "category": "Category X",
        "sum": 100,
    },
    {
        "id_company": 2,
        "product_name": "Product A",
        "description": "Description B",
        "category": "Category Y",
        "sum": 150,
    },
    {
        "id_company": 3,
        "product_name": "Product C",
        "description": "Description C",
        "category": "Category Z",
        "sum": 200,
    },
    {
        "id_company": 1,
        "product_name": "Product B",
        "description": "Description D",
        "category": "Category X",
        "sum": 120,
    },
    {
        "id_company": 5,
        "product_name": "Product E",
        "description": "Description B A",
        "category": "Category Y",
        "sum": 180,
    },
    {
        "id_company": 2,
        "product_name": "Product A",
        "description": "Description C",
        "category": "Category Z",
        "sum": 220,
    },
    {
        "id_company": 3,
        "product_name": "Product G",
        "description": "Description G N",
        "category": "Category X",
        "sum": 130,
    },
    {
        "id_company": 8,
        "product_name": "Product A",
        "description": "Description A",
        "category": "Category Y",
        "sum": 170,
    },
    {
        "id_company": 9,
        "product_name": "Product C",
        "description": "Description I",
        "category": "Category Z",
        "sum": 240,
    },
    {
        "id_company": 3,
        "product_name": "Product B",
        "description": "Description J",
        "category": "Category X",
        "sum": 110,
    },
]
