from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Comparison(Base):
    __tablename__ = "comparison"

    id = Column(Integer, primary_key=True, index=True)
    merged_analysis_id = Column(Integer, ForeignKey("merged_analysis.id"))
    comparison_notes = Column(String)
    created = Column(DateTime, default=datetime.utcnow)