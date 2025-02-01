from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analysis import Analysis
from app.schemas.__init__ import AnalysisCreate, AnalysisResponse

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
def create_analysis(analysis: AnalysisCreate, db: Session = Depends(get_db)):
    db_analysis = Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/", response_model=list[AnalysisResponse])
def get_analyses(db: Session = Depends(get_db)):
    return db.query(Analysis).all()