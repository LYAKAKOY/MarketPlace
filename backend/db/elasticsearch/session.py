from typing import Generator
import settings
from elasticsearch import AsyncElasticsearch

async def _get_db_es() -> Generator:
    elastic_client = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    try:
        yield elastic_client
    finally:
        await elastic_client.close()
