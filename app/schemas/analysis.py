from pydantic import BaseModel

class AnalysisCreate(BaseModel):
    note: str
    target_gv: int
    session_id: int
    catalog_id: int

class AnalysisResponse(BaseModel):
    id: int
    note: str
    target_gv: int
    session_id: int
    catalog_id: int

    model_config = {
        "from_attributes": True  # Using the new model_config dict instead of Config class
    }
