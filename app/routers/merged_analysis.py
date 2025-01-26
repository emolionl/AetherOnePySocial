# Example routers/merged_analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.merged_analysis import MergedAnalysis
from app.schemas.merged_analysis import MergedAnalysisCreate, MergedAnalysisResponse

router = APIRouter()

@router.post("/", response_model=MergedAnalysisResponse)
def create_merged_analysis(merged_analysis: MergedAnalysisCreate, db: Session = Depends(get_db)):
    db_merged_analysis = MergedAnalysis(**merged_analysis.dict())
    db.add(db_merged_analysis)
    db.commit()
    db.refresh(db_merged_analysis)
    return db_merged_analysis

@router.get("/", response_model=list[MergedAnalysisResponse])
def get_merged_analyses(db: Session = Depends(get_db)):
    return db.query(MergedAnalysis).all()