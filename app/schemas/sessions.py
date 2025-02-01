from pydantic import BaseModel

class SessionCreate(BaseModel):
    name: str
    description: str

class SessionResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = {
        "from_attributes": True
    }
