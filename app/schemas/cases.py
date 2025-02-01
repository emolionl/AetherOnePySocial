from pydantic import BaseModel

class CaseCreate(BaseModel):
    title: str
    description: str
    class Config:
        from_attributes = True

class CaseResponse(BaseModel):
    id: int
    title: str
    description: str

    model_config = {
        "from_attributes": True
    }
