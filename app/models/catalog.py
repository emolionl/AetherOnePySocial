from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    author = Column(String)
    import_date = Column(DateTime, default=datetime.utcnow)