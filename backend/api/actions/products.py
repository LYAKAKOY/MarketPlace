from typing import List

import settings
from api.products.schemas import CreateProduct
from api.products.schemas import ScrollListProducts
from api.products.schemas import ShowProduct
from db.elasticsearch.indexes import NAME_INDEX_PRODUCTS
from elasticsearch import AsyncElasticsearch


async def _create_product(
    product: CreateProduct, elastic_client: AsyncElasticsearch
) -> ShowProduct | None:
    res = await elastic_client.index(
        index=NAME_INDEX_PRODUCTS,
        document=product.model_dump(exclude_none=True),
        refresh=True,
    )
    if res.meta.status == 201:
        return ShowProduct(
            id_product=res.get("_id"), **product.model_dump(exclude_none=True)
        )


async def _get_all_products(
    elastic_client: AsyncElasticsearch,
) -> ScrollListProducts | None:
    res = await elastic_client.search(
        index=NAME_INDEX_PRODUCTS, query={"match_all": {}}, scroll=settings.SCROLL_TIME
    )
    if res.meta.status == 200:
        scroll_id = res["_scroll_id"]
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)


async def _get_all_products_by_category(
    category: str, elastic_client: AsyncElasticsearch
) -> ScrollListProducts | None:
    res = await elastic_client.search(
        index=NAME_INDEX_PRODUCTS,
        query={"term": {"category.keyword": {"value": category}}},
        scroll=settings.SCROLL_TIME,
    )
    if res.meta.status == 200:
        scroll_id = res["_scroll_id"]
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)


async def _get_all_product_by_company_id(
    id_company: int, elastic_client: AsyncElasticsearch
) -> List[ShowProduct] | None:
    res = await elastic_client.search(
        index=NAME_INDEX_PRODUCTS,
        query={"term": {"id_company": {"value": id_company}}},
        scroll=settings.SCROLL_TIME,
    )
    if res.meta.status == 200:
        scroll_id = res["_scroll_id"]
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)


async def _get_products_by_scroll(
    scroll_id: str, elastic_client: AsyncElasticsearch
) -> ScrollListProducts | None:
    res = await elastic_client.options(ignore_status=400).scroll(
        scroll_id=scroll_id, scroll=settings.SCROLL_TIME
    )
    if res.meta.status == 200:
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)


async def _get_products_using_filter(
    product_name: str, min_sum: int, max_sum: int, elastic_client: AsyncElasticsearch
) -> ScrollListProducts | None:
    res = await elastic_client.search(
        index=NAME_INDEX_PRODUCTS,
        query={
            "bool": {
                "must": [
                    {"term": {"product_name.keyword": {"value": product_name}}},
                    {"range": {"sum": {"gte": min_sum, "lt": max_sum}}},
                ]
            }
        },
        scroll=settings.SCROLL_TIME,
    )
    if res.meta.status == 200:
        scroll_id = res["_scroll_id"]
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)


async def _get_products_by_match_description(
    description: str, elastic_client: AsyncElasticsearch
) -> List[ShowProduct] | None:
    res = await elastic_client.search(
        index=NAME_INDEX_PRODUCTS,
        query={"match": {"description": {"query": description}}},
        scroll=settings.SCROLL_TIME,
    )
    if res.meta.status == 200:
        scroll_id = res["_scroll_id"]
        products = res.get("hits").get("hits")
        if products:
            list_show_products = [
                ShowProduct(id_product=product.get("_id"), **product.get("_source"))
                for product in products
            ]
            return ScrollListProducts(scroll_id=scroll_id, products=list_show_products)
