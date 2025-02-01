from pydantic import BaseModel

class CatalogCreate(BaseModel):
    name: str
    description: str

class CatalogResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = {
        "from_attributes": True
    }
