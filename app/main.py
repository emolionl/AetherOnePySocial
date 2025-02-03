from fastapi import FastAPI, Depends
from app.database import Base, engine, init_db
from app.routers import auth, keys, analysis, utils
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User
from app.routers import analysis
from app.routers.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    # This will treat URLs with and without trailing slashes as the same
    redirect_slashes=True
)

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
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(keys.router, prefix="/api/keys", tags=["keys"])
app.include_router(utils.router, prefix="/api/utils", tags=["utils"])

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