from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, machines, catalog, rates, cases, sessions, analysis, merged_analysis, comparison
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(machines.router, prefix="/api/machines", tags=["Machines"])
app.include_router(catalog.router, prefix="/api/catalog", tags=["Catalog"])
app.include_router(rates.router, prefix="/api/rates", tags=["Rates"])
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(merged_analysis.router, prefix="/api/merged-analysis", tags=["Merged Analysis"])
app.include_router(comparison.router, prefix="/api/comparison", tags=["Comparison"])

def run_server():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload
        reload_dirs=["app"]  # Watch the 'app' directory for changes
    )