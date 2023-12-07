from typing import Generator
import settings
from elasticsearch import AsyncElasticsearch

async def get_test_db_es() -> Generator:
    test_elastic_client = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    try:
        yield test_elastic_client
    finally:
        await test_elastic_client.close()