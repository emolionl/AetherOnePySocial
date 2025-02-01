from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.catalog import Catalog
from app.schemas.__init__ import CatalogCreate, CatalogResponse

router = APIRouter()

@router.post("/", response_model=CatalogResponse)
def create_catalog(catalog: CatalogCreate, db: Session = Depends(get_db)):
    db_catalog = Catalog(**catalog.dict())
    db.add(db_catalog)
    db.commit()
    db.refresh(db_catalog)
    return db_catalog

@router.get("/", response_model=list[CatalogResponse])
def get_catalogs(db: Session = Depends(get_db)):
    return db.query(Catalog).all()