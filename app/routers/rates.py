from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rate import Rate
from app.schemas.rate import RateCreate, RateResponse

router = APIRouter()

@router.post("/", response_model=RateResponse)
def create_rate(rate: RateCreate, db: Session = Depends(get_db)):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

@router.get("/", response_model=list[RateResponse])
def get_rates(db: Session = Depends(get_db)):
    return db.query(Rate).all()