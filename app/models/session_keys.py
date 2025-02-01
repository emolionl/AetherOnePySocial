from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class SessionKey(Base):
    __tablename__ = "session_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    key = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    session_id = Column(Integer)
    local_session_id = Column(Integer)
    used = Column(Boolean, nullable=False, default=False, server_default='false')
    used_at = Column(DateTime, nullable=True) 

    # Ensure the combination of user_id and key is unique
    __table_args__ = (
        UniqueConstraint('user_id', 'key', 'local_session_id', name='_user_key_local_session_id_uc'),
    )
