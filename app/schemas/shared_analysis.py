from pydantic import BaseModel
from typing import Optional, Any

class SharedAnalysisResponse(BaseModel):
    id: int
    user_id: int
    machine_id: str
    key_id: Optional[int]
    key: str
    raw: dict[str, Any]

    model_config = {
        "from_attributes": True
    } 