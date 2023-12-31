from api.actions.products import _create_product
from api.actions.products import _get_all_product_by_company_id
from api.actions.products import _get_all_products
from api.actions.products import _get_all_products_by_category
from api.actions.products import _get_products_by_match_description
from api.actions.products import _get_products_by_scroll
from api.actions.products import _get_products_using_filter
from api.products.schemas import CreateProduct
from api.products.schemas import ScrollListProducts
from api.products.schemas import ShowProduct
from db.elasticsearch.session import get_db_es
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

products_router = APIRouter()


@products_router.post("/", response_model=ShowProduct)
async def create_product(
    body: CreateProduct, elastic_client: AsyncElasticsearch = Depends(get_db_es)
) -> ShowProduct:
    res = await _create_product(body, elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="the server is not responding",
        )
    return res


@products_router.get("/", response_model=ScrollListProducts)
async def get_products(
    elastic_client: AsyncElasticsearch = Depends(get_db_es),
) -> ScrollListProducts:
    res = await _get_all_products(elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res


@products_router.get("/by_category/{category}", response_model=ScrollListProducts)
async def get_products_by_category(
    category: str, elastic_client: AsyncElasticsearch = Depends(get_db_es)
) -> ScrollListProducts:
    res = await _get_all_products_by_category(category, elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res


@products_router.get("/by_company/{company_id}", response_model=ScrollListProducts)
async def get_products_by_company_id(
    company_id: int, elastic_client: AsyncElasticsearch = Depends(get_db_es)
) -> ScrollListProducts:
    res = await _get_all_product_by_company_id(company_id, elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res


@products_router.get(
    "/by_match_description/{description}", response_model=ScrollListProducts
)
async def get_products_by_match_description(
    description: str, elastic_client: AsyncElasticsearch = Depends(get_db_es)
) -> ScrollListProducts:
    res = await _get_products_by_match_description(description, elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res


@products_router.get("/filter", response_model=ScrollListProducts)
async def get_products_using_filter(
    product_name: str,
    max_sum: int,
    min_sum: int = 0,
    elastic_client: AsyncElasticsearch = Depends(get_db_es),
) -> ScrollListProducts:
    res = await _get_products_using_filter(
        product_name=product_name,
        min_sum=min_sum,
        max_sum=max_sum,
        elastic_client=elastic_client,
    )
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res


@products_router.get("/scroll/{scroll_id}", response_model=ScrollListProducts)
async def get_products_by_scroll_id(
    scroll_id: str, elastic_client: AsyncElasticsearch = Depends(get_db_es)
) -> ScrollListProducts:
    res = await _get_products_by_scroll(scroll_id, elastic_client)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no products"
        )
    return res
