from api.products.handlers import products_router
from fastapi import APIRouter
from fastapi import FastAPI
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

app = FastAPI(description="The Best MarketPlace")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

main_api_router = APIRouter()
main_api_router.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(main_api_router)
