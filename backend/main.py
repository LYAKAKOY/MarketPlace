from fastapi import FastAPI, APIRouter

from api.products.handlers import products_router

app = FastAPI(description="The Best MarketPlace")

main_api_router = APIRouter()
main_api_router.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(main_api_router)