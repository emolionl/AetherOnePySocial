from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from app.database import get_db
from app.models.cases import Case
from app.models.sessions import Session as SessionModel
from app.models.analysis import Analysis
from app.models.rate_analysis import RateAnalysis
from app.models.catalog import Catalog
from app.models.session_raw import SessionRaw
from app.schemas.shared_analysis import SharedAnalysisResponse
from app.models.session_keys import SessionKey
from app.routers.auth import get_current_user
from app.models.user import User
from uuid import UUID
import logging

router = APIRouter()

# Set up logging at the top of the file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def create_shared_analysis(
    data: Dict[Any, Any], 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Received data: {data}")
        
        # Verify the user_id matches the authenticated user
        if data["data"]["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to create analysis for other users")

        # Check if session key exists and is valid
        session_key = db.query(SessionKey).filter(
            SessionKey.key == data["data"]["key"],
            #SessionKey.user_id == data["data"]["user_id"]
        ).first()
        logger.info(f"Found session key: {session_key}")

        if not session_key:
            logger.warning(f"Session key not found for key: {data['data']['key']}")
            raise HTTPException(status_code=404, detail="Invalid session key")

        # Check for existing entry
        existing = db.query(SessionRaw).filter(
            SessionRaw.user_id == data["data"]["user_id"],
            SessionRaw.machine_id == data["data"]["machine_id"],
            SessionRaw.key == data["data"]["key"]
        ).first()

        if existing:
            return {
                "status": "skipped",
                "message": "Analysis with same user_id, machine_id, and key already exists",
                "existing_id": existing.id
            }

        # Save raw data with session key id
        raw_session = SessionRaw(
            user_id=data["data"]["user_id"],
            machine_id=data["data"]["machine_id"],
            key=data["data"]["key"],
            key_id=session_key.id,  # Set the session key id
            raw=data
        )
        db.add(raw_session)
        db.flush()

        # Extract main data
        analysis_data = data["data"]["analyses"]
        machine_id = data["data"]["machine_id"]
        user_id = data["data"]["user_id"]
        
        # Create or update case
        case_data = analysis_data["case"]
        logger.info(f"Processing case data: {case_data}")
        case = Case(
            local_id=case_data["id"],  # Store original ID as local_id
            machine_id=machine_id,
            name=case_data["name"],
            description=case_data["description"],
            email=case_data["email"],
            color=case_data["color"],
            created=datetime.fromisoformat(case_data["created"]),
            last_change=datetime.strptime(case_data["last_change"], "%a, %d %b %Y %H:%M:%S GMT")
        )
        db.add(case)  # Use add instead of merge since we're creating new records
        db.flush()  # This will assign the new server ID
        
        # Create or update session
        session_data = analysis_data["session"]
        session = SessionModel(
            local_id=session_data["id"],
            machine_id=machine_id,
            case_id=case.id,  # Use the new server-side case ID
            user_id=user_id,  # Add user_id to the session
            description=session_data["description"],
            intention=session_data["intention"],
            created=datetime.fromisoformat(session_data["created"]),
            key_id=session_key.id
        )
        db.add(session)
        db.flush()


        # Process each analysis
        analysis_ids = []
        for analysis_item in analysis_data["analyses"]:
            # Create or update catalog first
            catalog_info = analysis_item["catalog"]
            catalog = Catalog(
                id=catalog_info["id"],
                name=catalog_info["name"],
                description=catalog_info["description"]
            )
            db.merge(catalog)  # Use merge to handle both insert and update
            db.flush()

            # Then create the analysis with the existing catalog
            analysis_info = analysis_item["analysis"]
            analysis = Analysis(
                local_id=analysis_info["id"],
                machine_id=machine_id,
                session_id=session.id,  # Use the new server-side session ID
                catalog_id=analysis_info["catalog_id"],
                target_gv=analysis_info["target_gv"],
                created=datetime.fromisoformat(analysis_info["created"])
            )
            db.add(analysis)
            db.flush()
            analysis_ids.append(analysis.id)

            # Create or update catalog if needed
            catalog_info = analysis_item["catalog"]
            catalog = Catalog(
                id=catalog_info["id"],  # Catalog IDs might be consistent across installations
                name=catalog_info["name"],
                description=catalog_info["description"]
            )
            db.merge(catalog)  # Use merge for catalog as it might already exist

            # Create or update rate analyses
            for rate_analysis in analysis_item["rate_analysis"]:
                rate = RateAnalysis(
                    local_id=rate_analysis["id"],
                    machine_id=machine_id,
                    analysis_id=analysis.id,  # Use the new server-side analysis ID
                    catalog_id=rate_analysis["catalog_id"],
                    signature=rate_analysis["signature"],
                    description=rate_analysis["description"],
                    energetic_value=rate_analysis["energetic_value"],
                    gv=rate_analysis["gv"],
                    level=rate_analysis["level"],
                    potencyType=rate_analysis["potencyType"],
                    potency=rate_analysis["potency"],
                    note=rate_analysis["note"]
                )
                db.add(rate)
        session_key.used = True
        session_key.used_at = datetime.utcnow()
        session_key.session_id = session.id
        #session_key.local_session_id = data.get('session_id')  # This is the local session ID from the client
        
        # Commit all changes
        db.commit()

        return {
            "status": "success",
            "message": "Shared analysis data saved successfully",
            "new_ids": {
                "raw_session_id": raw_session.id,
                "case_id": case.id,
                "session_id": session.id,
                "analysis_ids": analysis_ids
            }
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error in create_shared_analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error saving shared analysis: {str(e)}"
        )


@router.get("/by-key/{key}")
def get_analyses_by_key(
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