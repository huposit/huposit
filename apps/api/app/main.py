from fastapi import FastAPI

from app.core.cors import setup_cors
from app.features.auth.router import router as auth_router
from app.features.health.router import router as health_router

from app.core.errors import setup_exception_handlers

app = FastAPI(title="Huposit API")

setup_cors(app)
setup_exception_handlers(app)

app.include_router(auth_router)
app.include_router(health_router)
