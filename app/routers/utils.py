from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session_raw import SessionRaw
from app.models.sessions import Session
from app.models.analysis import Analysis
from app.models.rate_analysis import RateAnalysis
from app.models.cases import Case
from app.models.user import User
from app.models.session_keys import SessionKey

router = APIRouter()

@router.post("/clear-data")
def clear_tables(db: Session = Depends(get_db)):
    # Delete in correct order due to foreign key constraints
    db.query(RateAnalysis).delete()
    db.query(Analysis).delete()
    db.query(Session).delete()
    db.query(Case).delete()
    db.query(SessionRaw).delete()
    db.query(SessionKey).delete()
    db.query(User).delete()
    db.commit()
    return {"message": "All data cleared"} 