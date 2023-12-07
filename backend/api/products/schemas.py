from pydantic import BaseModel, Extra, ConfigDict

from api.base_schemas import TunedModel


class CreateProduct(BaseModel):
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int

    class Config:
        strict = True
        extra = Extra.allow

class ShowProduct(TunedModel):
    id_product: str
    id_company: int
    product_name: str
    description: str
    category: str
    sum: int

    class Config:
        extra = Extra.allow