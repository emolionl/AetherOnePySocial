from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import all your models here
from app.models.analysis import Analysis
from app.models.cases import Case
from app.models.catalog import Catalog
from app.models.rate_analysis import RateAnalysis
from app.models.rate import Rate
from app.models.session_keys import SessionKey
from app.models.sessions import Session
from app.models.session_raw import SessionRaw
from app.models.user import User

# Add other models as needed
def init_db():
    import app.models  # Import all models
    Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()