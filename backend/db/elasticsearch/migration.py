import asyncio
import os
from elasticsearch import AsyncElasticsearch
from indexes import all_indexes

es_database_url = f"http://{os.environ.get('ES_DATABASE')}:{os.environ.get('ES_PORT')}"

async def create_index(name_index: str, mappings: dict):
    elastic_client = AsyncElasticsearch(hosts=es_database_url)
    await elastic_client.indices.create(index=name_index, mappings=mappings)
    await elastic_client.close()

async def migrations():

    tasks = [asyncio.create_task(create_index(name_index=key, mappings=value))
                                 for key, value in all_indexes.items()]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(migrations())