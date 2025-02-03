import os
from fastapi import APIRouter, Depends, HTTPException
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

# Get the environment from an environment variable
ENV = os.getenv('ENV', 'development')  # Default to 'development' if not set

def clear_database(db):
    if ENV != 'development':
        raise HTTPException(status_code=403, detail="Operation not allowed in production")

    db.query(RateAnalysis).delete()
    db.query(Analysis).delete()
    db.query(Session).delete()
    db.query(Case).delete()
    db.query(SessionRaw).delete()
    db.query(SessionKey).delete()
    db.query(User).delete()
    db.commit()

@router.post("/clear-data")
def clear_tables(db: Session = Depends(get_db)):
    clear_database(db)
    return {"message": "All data cleared"} 