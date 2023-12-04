from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from api.actions.products import _create_product, _get_all_products
from db.elasticsearch.session import get_db_es
from api.products.schemas import CreateProduct, ShowProduct

products_router = APIRouter()


@products_router.post("/", response_model=ShowProduct)
async def create_product(body: CreateProduct,
                         elastic_client: AsyncElasticsearch = Depends(get_db_es)) -> ShowProduct:
    """create product"""
    res = await _create_product(body, elastic_client)
    if res is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="the server is not responding")
    return res

@products_router.get("/")
async def get_products(elastic_client: AsyncElasticsearch = Depends(get_db_es)):
    """create product"""
    res = await _get_all_products(elastic_client)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no products")
    return res