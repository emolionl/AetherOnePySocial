from fastapi import FastAPI, Depends
from app.database import Base, engine, init_db
from app.routers import auth,  catalog, rates, cases, sessions, analysis, shared_analysis, utils, session_keys
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.routers.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
#init_db() # no need, because we are going via alembic

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
#app.include_router(catalog.router, prefix="/api/catalog", tags=["Catalog"])
#app.include_router(rates.router, prefix="/api/rates", tags=["Rates"])
#app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
#app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
#app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(shared_analysis.router, prefix="/api/shared-analysis", tags=["shared-analysis"])
app.include_router(utils.router, prefix="/api/utils", tags=["utils"])
app.include_router(session_keys.router, prefix="/api/session-keys", tags=["session-keys"])
# def find_pydantic_models():
#     for cls in BaseModel.__subclasses__():
#         print(f"Model: {cls.__name__}")
#         if hasattr(cls, 'Config'):
#             print(f"  Has Config class with attributes: {dir(cls.Config)}")
#         if hasattr(cls, 'model_config'):
#             print(f"  Has model_config: {cls.model_config}")

# find_pydantic_models()

@app.get("/")
async def root():
    return {"message": "Welcome to AetherOnePySocial API"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

@auth.router.get("/protected-route")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}

def run_server():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload
        reload_dirs=["app"]  # Watch the 'app' directory for changes
    )