from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comparison import Comparison
from app.schemas.comparison import ComparisonCreate, ComparisonResponse

router = APIRouter()

@router.post("/", response_model=ComparisonResponse)
def create_comparison(comparison: ComparisonCreate, db: Session = Depends(get_db)):
    db_comparison = Comparison(**comparison.dict())
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    return db_comparison

@router.get("/", response_model=list[ComparisonResponse])
def get_comparisons(db: Session = Depends(get_db)):
    return db.query(Comparison).all()