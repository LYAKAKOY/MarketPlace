from pydantic import BaseModel, Extra


class TunedModel(BaseModel):
    class ConfigDict:
        from_attributes = True