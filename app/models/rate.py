from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    signature = Column(String, unique=True)
    description = Column(String)
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
