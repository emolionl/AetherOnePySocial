from pydantic import BaseModel

class CaseCreate(BaseModel):
    name: str
    email: str
    color: str
    description: str

class CaseResponse(BaseModel):
    id: int
    name: str
    email: str
    color: str
    description: str

    class Config:
        orm_mode = True