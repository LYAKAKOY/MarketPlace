from typing import List

from api.base_schemas import TunedModel
from pydantic import BaseModel, ConfigDict, Extra


class CreateProduct(BaseModel):
    model_config = ConfigDict(strict=True, extra="allow")
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int


class ShowProduct(TunedModel):
    model_config = ConfigDict(extra="allow")
    id_product: str
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int


class ScrollListProducts(TunedModel):
    scroll_id: str
    products: List[ShowProduct]
