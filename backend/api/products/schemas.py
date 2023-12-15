from typing import List

from pydantic import BaseModel

from api.base_schemas import TunedModel


class CreateProduct(BaseModel):
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int

    class Config:
        strict = True
        extra = 'allow'


class ShowProduct(TunedModel):
    id_product: str
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int

    class Config:
        extra = 'allow'


class ScrollListProducts(TunedModel):
    scroll_id: str
    products: List[ShowProduct]
