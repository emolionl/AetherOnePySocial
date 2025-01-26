from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class MergedAnalysis(Base):
    __tablename__ = "merged_analysis"

    id = Column(Integer, primary_key=True, index=True)
    analysis_ids = Column(String)  # Comma-separated list of analysis IDs
    user_id = Column(Integer, ForeignKey("users.id"))
    merged_at = Column(DateTime, default=datetime.utcnow)