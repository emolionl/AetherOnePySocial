from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, nullable=True)  # ID from local machine
    machine_id = Column(String, nullable=True)
    note = Column(String)
    target_gv = Column(Integer)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    created = Column(DateTime, default=datetime.utcnow)