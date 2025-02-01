from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/users/")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user