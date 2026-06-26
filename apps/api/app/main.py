from fastapi import FastAPI

from app.core.cors import setup_cors
from app.features.auth.router import router as auth_router
from app.features.health.router import router as health_router

app = FastAPI(title="Huposit API")

setup_cors(app)

app.include_router(auth_router)
app.include_router(health_router)
