from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.session_keys import SessionKey
from app.models.user import User
from app.routers.auth import get_current_user
import uuid
from typing import Optional
from uuid import UUID
from app.models.sessions import Session

class SessionKeyCreate(BaseModel):
    user_id: int
    local_session_id: int
    key: Optional[str] = None
    session_id: Optional[UUID] = None

router = APIRouter()

@router.post("/")
def create_key(
    data: SessionKeyCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the authenticated user matches the requested user_id
    if current_user.id != data.user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create/update session keys for other users"
        )
    # Validate required fields
    if not data.local_session_id or not data.user_id:
        raise HTTPException(
            status_code=400,
            detail="local_session_id and user_id are required fields"
        )

    # Validate UUID format if key is provided
    if data.key:
        try:
            UUID(data.key)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid key format. Must be a valid UUID"
            )
    
    # Check if exact combination already exists
    if data.key:  # Only check if key is provided
        existing_combination = db.query(SessionKey).filter(
            SessionKey.user_id == data.user_id,
            SessionKey.key == data.key,
            SessionKey.local_session_id == data.local_session_id
        ).first()
        
        if existing_combination:
            return {
                "status": "error",
                "message": "This combination of user_id, key, and local_session_id already exists. This is not allowed.",
                "user_id": data.user_id,
                "key": data.key,
                "local_session_id": data.local_session_id
            }

    # Check if user already has any key
    existing_key = db.query(SessionKey).filter(
        SessionKey.user_id == data.user_id,
        SessionKey.local_session_id == data.local_session_id
    ).first()
    
    if existing_key:
        return {
            "status": "exists",
            "message": "Session key already exists for this user in combination with local_session_id",
            "key": existing_key.key,
            "user_id": existing_key.user_id,
            "local_session_id": existing_key.local_session_id
        }
    
    # Create new key if no conflicts exist
    session_key = SessionKey(
        user_id=data.user_id,
        local_session_id=data.local_session_id,
        key=data.key or str(uuid.uuid4()),
        used=False,
    )
    db.add(session_key)
    db.commit()
    db.refresh(session_key)
    
    return {
        "status": "created",
        "message": "New session key created successfully",
        "key": session_key.key,
        "user_id": session_key.user_id,
        "local_session_id": session_key.local_session_id
    }

@router.get("/")
def get_my_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_keys = db.query(SessionKey).filter(SessionKey.user_id == current_user.id).all()
    return session_keys

@router.get("/{key_id}")
def get_my_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):


    session_key = db.query(SessionKey).filter(SessionKey.id == key_id, SessionKey.user_id == current_user.id).first()
    if not session_key:
        raise HTTPException(status_code=404, detail="Session key not found")
    return session_key
