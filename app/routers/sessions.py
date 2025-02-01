from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sessions import Session as SessionModel
from app.schemas.__init__ import SessionCreate, SessionResponse

router = APIRouter()

@router.post("/", response_model=SessionResponse)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = SessionModel(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=list[SessionResponse])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).all()