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
from datetime import datetime
from fastapi import Body

class SessionKeyCreate(BaseModel):
    user_id: int
    local_session_id: int
    key: Optional[str] = None
    session_id: Optional[UUID] = None

class SessionKeyUpdateUsed(BaseModel):
    used: bool
    used_at: Optional[datetime] = None

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
                "key_id": data.id,
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
            "key_id": existing_key.id,
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
        "key_id": session_key.id,
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

@router.get("/{id_or_key}")
def get_key_or_keys(
    id_or_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Try to interpret as integer (user_id)
    try:
        user_id = int(id_or_key)
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # Get all sessions for this user
        user_sessions = db.query(Session).filter(Session.user_id == user_id).all()
        
        # Get all keys associated with these sessions
        session_keys = []
        for session in user_sessions:
            # Get the key for this session
            key = db.query(SessionKey).filter(SessionKey.id == session.key_id).first()
            if key:
                session_keys.append({
                    "id": key.id,
                    "key": str(key.key),
                    "user_id": key.user_id,
                    "my_key": key.user_id == current_user.id,
                    "session_id": session.id,
                    "local_session_id": session.local_id
                })
        
        # Get direct keys owned by the user
        direct_keys = db.query(SessionKey).filter(SessionKey.user_id == user_id).all()
        direct_keys_list = [{
            "id": k.id,
            "key": str(k.key),
            "user_id": k.user_id,
            "my_key": True,
            "session_id": None,
            "local_session_id": None
        } for k in direct_keys]
        
        # Combine both lists
        all_keys = direct_keys_list + session_keys
        
        if not all_keys:
            raise HTTPException(status_code=404, detail="No session keys found")
            
        return all_keys
        
    except ValueError:
        # Not an int, try as UUID key (SessionKey.key)
        try:
            key_uuid = UUID(id_or_key)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid key format")
        session_key = db.query(SessionKey).filter(SessionKey.key == key_uuid, SessionKey.user_id == current_user.id).first()
        if not session_key:
            raise HTTPException(status_code=404, detail="Session key not found")
        return [{
            "id": session_key.id,
            "key": str(session_key.key),
            "user_id": session_key.user_id,
            "my_key": True,
            "session_id": None,
            "local_session_id": None
        }]

@router.patch("/use/{key}")
def update_session_key_used(
    key: str,
    data: SessionKeyUpdateUsed,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_key = db.query(SessionKey).filter(SessionKey.key == key, SessionKey.user_id == current_user.id).first()
    if not session_key:
        raise HTTPException(status_code=404, detail="Session key not found")
    session_key.used = data.used
    if data.used_at is not None:
        session_key.used_at = data.used_at
    elif data.used:
        session_key.used_at = datetime.utcnow()
    db.commit()
    db.refresh(session_key)
    return {
        "status": "success",
        "key": str(session_key.key),
        "used": session_key.used,
        "used_at": session_key.used_at
    }
