from pydantic import BaseModel
from typing import Optional

class SessionKeyCreate(BaseModel):
    key: str
    session_id: int

class SessionKeyResponse(BaseModel):
    id: int
    user_id: int
    key: str

    model_config = {
        "from_attributes": True
    }
