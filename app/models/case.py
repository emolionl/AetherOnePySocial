from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    color = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    last_change = Column(DateTime, default=datetime.utcnow)