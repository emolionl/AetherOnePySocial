from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rate_analysis import Rate
from app.schemas.__init__ import RateCreate, RateResponse

router = APIRouter()

@router.post("/rates/", response_model=RateResponse)
def create_rate(rate: RateCreate, db: Session = Depends(get_db)):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate 