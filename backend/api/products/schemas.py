from pydantic import BaseModel, Extra

from api.base_schemas import TunedModel


class CreateProduct(BaseModel):
    id_company: int
    product_name: str
    description: str
    sum: int

    class Config:
        extra = Extra.allow

class ShowProduct(TunedModel):
    id_product: str
    id_company: int
    product_name: str
    description: str
    sum: int

    class Config:
        extra = Extra.allow