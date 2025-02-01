from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from app.database import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, nullable=True)  # ID from local machine
    machine_id = Column(String, nullable=True)
    intention = Column(String)
    description = Column(String)
    case_id = Column(Integer, ForeignKey("cases.id"))
    key_id = Column(Integer, ForeignKey("session_keys.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created = Column(DateTime, default=datetime.utcnow)


    # Add a unique constraint on key_id, user_id, and machine_id
    __table_args__ = (
        UniqueConstraint('key_id', 'user_id', 'machine_id', name='_key_user_machine_uc'),
    )