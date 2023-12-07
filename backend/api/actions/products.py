from typing import List

from elasticsearch import AsyncElasticsearch

from api.products.schemas import CreateProduct, ShowProduct
from db.elasticsearch.indexes import NAME_INDEX_PRODUCTS


async def _create_product(product: CreateProduct, elastic_client: AsyncElasticsearch) -> ShowProduct | None:
    res = await elastic_client.index(index=NAME_INDEX_PRODUCTS, document=product.model_dump(exclude_none=True,
                                                                        exclude={'additionalProp1'}))
    if res.meta.status == 201:
        return ShowProduct(id_product=res.get("_id"), **product.model_dump(exclude_none=True,
                                                                        exclude={'additionalProp1'}))

async def _get_all_products(elastic_client: AsyncElasticsearch) -> List[ShowProduct] | None:
    res = await elastic_client.search(index=NAME_INDEX_PRODUCTS, query={"match_all": {}})
    products = res.get("hits").get("hits")
    if products is not None:
        list_show_products = [ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                              for product in products]
        return list_show_products

async def _get_all_products_by_category(category: str, elastic_client: AsyncElasticsearch) -> List[ShowProduct] | None:
    res = await elastic_client.search(index=NAME_INDEX_PRODUCTS, query={"match": {"category": {"query": category}}})
    products = res.get("hits").get("hits")
    if products is not None:
        list_show_products = [ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                              for product in products]
        return list_show_products

async def _get_all_product_by_company_id(id_company: int, elastic_client: AsyncElasticsearch) -> List[ShowProduct] | None:
    res = await elastic_client.search(index=NAME_INDEX_PRODUCTS, query={"term": {"id_company": {"value": id_company}}})
    products = res.get("hits").get("hits")
    if products is not None:
        list_show_products = [ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                              for product in products]
        return list_show_products