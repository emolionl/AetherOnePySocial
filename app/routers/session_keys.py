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
from app.models.sessions import Session as SessionModel
from app.models.analysis import Analysis
from app.models.rate_analysis import RateAnalysis
from app.models.catalog import Catalog
from app.models.cases import Case



class SessionKeyCreate(BaseModel):
    user_id: int
    local_session_id: int
    key: Optional[str] = None
    session_id: Optional[UUID] = None

router = APIRouter()

@router.post("/")
def create_session_key(
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


@router.get("/my-session-keys")
def get_my_session_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):


    session_keys = db.query(SessionKey).filter(SessionKey.user_id == current_user.id).all()
    return session_keys

@router.get("/my-session-keys/{key_id}")
def get_my_session_key(
    key_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    session_key = db.query(SessionKey).filter(SessionKey.id == key_id, SessionKey.user_id == current_user.id).first()
    if not session_key:
        raise HTTPException(status_code=404, detail="Session key not found")
    return session_key

@router.get("/my-session-connected-keys/{key}")
def get_my_session_connected_keys(
    key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    print(f"Key: {key}")
    # First, get the session key record
    session_key = db.query(SessionKey).filter(SessionKey.key == key).first()
    if not session_key:
        raise HTTPException(status_code=404, detail="Session key not found")

    # Check if there's a session with this key_id and current user
    session_exists = db.query(SessionModel).filter(
        SessionModel.key_id == session_key.id,
        SessionModel.user_id == current_user.id
    ).first()


    if not session_exists:
        raise HTTPException(
            status_code=403, 
            detail="No sessions found for this key and user combination"
        )

    # Get all sessions for this key
    sessions = db.query(SessionModel).filter(
        SessionModel.key_id == session_key.id
    ).all()

    response_data = []
    for session in sessions:
        # Get all analyses for this session
        analyses = db.query(Analysis).filter(
            Analysis.session_id == session.id
        ).all()

        analyses_data = []
        for analysis in analyses:
            # Get all rate analyses for this analysis
            rate_analyses = db.query(RateAnalysis).filter(
                RateAnalysis.analysis_id == analysis.id
            ).all()

            # Get catalog info for this analysis
            catalog = db.query(Catalog).filter(
                Catalog.id == analysis.catalog_id
            ).first()

            analyses_data.append({
                "id": analysis.id,
                "local_id": analysis.local_id,
                "machine_id": analysis.machine_id,
                "catalog_id": analysis.catalog_id,
                "target_gv": analysis.target_gv,
                "created": analysis.created.isoformat(),
                "catalog": {
                    "id": catalog.id,
                    "name": catalog.name,
                    "description": catalog.description
                } if catalog else None,
                "rate_analyses": [{
                    "id": rate.id,
                    "local_id": rate.local_id,
                    "machine_id": rate.machine_id,
                    "catalog_id": rate.catalog_id,
                    "signature": rate.signature,
                    "description": rate.description,
                    "energetic_value": rate.energetic_value,
                    "gv": rate.gv,
                    "level": rate.level,
                    "potencyType": rate.potencyType,
                    "potency": rate.potency,
                    "note": rate.note
                } for rate in rate_analyses]
            })

        # Get case info for this session
        case = db.query(Case).filter(Case.id == session.case_id).first()

        session_data = {
            "id": session.id,
            "local_id": session.local_id,
            "machine_id": session.machine_id,
            "user_id": session.user_id,
            "description": session.description,
            "intention": session.intention,
            "created": session.created.isoformat(),
            "case": {
                "id": case.id,
                "local_id": case.local_id,
                "name": case.name,
                "description": case.description,
                "email": case.email,
                "color": case.color,
                "created": case.created.isoformat(),
                "last_change": case.last_change.isoformat()
            } if case else None,
            "analyses": analyses_data
        }
        response_data.append(session_data)

    return {
        "status": "success",
        "status_code": 200,
        "message": "Sessions retrieved successfully",
        "data": response_data
    }