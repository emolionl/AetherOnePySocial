from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database import Base

class RateAnalysis(Base):
    __tablename__ = "rate_analysis"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, nullable=True)  # ID from local machine
    machine_id = Column(String, nullable=True)
    signature = Column(String)
    description = Column(String)
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    analysis_id = Column(Integer, ForeignKey("analysis.id"))
    energetic_value = Column(Integer)
    gv = Column(Integer)
    level = Column(Integer)
    potencyType = Column(String)
    potency = Column(Integer)
    note = Column(Text, nullable=True)
    
