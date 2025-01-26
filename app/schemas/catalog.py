from pydantic import BaseModel

class CatalogCreate(BaseModel):
    name: str
    description: str
    author: str

class CatalogResponse(BaseModel):
    id: int
    name: str
    description: str
    author: str

    class Config:
        orm_mode = True