from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.database import Base

class SessionRaw(Base):
    __tablename__ = "session_raw"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    machine_id = Column(String, nullable=False)
    key_id = Column(Integer, ForeignKey("session_keys.id"))
    key = Column(String, nullable=False)
    raw = Column(JSON, nullable=False) 