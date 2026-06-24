from fastapi import FastAPI
from app.features.health.router import router as health_router

app = FastAPI(title="Huposit API")

app.include_router(health_router)
