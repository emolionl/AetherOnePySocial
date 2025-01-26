from pydantic import BaseModel

class SessionCreate(BaseModel):
    intention: str
    description: str
    case_id: int

class SessionResponse(BaseModel):
    id: int
    intention: str
    description: str
    case_id: int

    class Config:
        orm_mode = True