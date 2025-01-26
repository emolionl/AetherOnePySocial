from pydantic import BaseModel

class ComparisonCreate(BaseModel):
    merged_analysis_id: int
    comparison_notes: str

class ComparisonResponse(BaseModel):
    id: int
    merged_analysis_id: int
    comparison_notes: str

    class Config:
        orm_mode = True