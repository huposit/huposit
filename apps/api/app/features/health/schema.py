# schema.py
from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]


class DatabaseHealthResponse(BaseModel):
    status: Literal["ok", "error"]
    database: Literal["connected", "disconnected"]


class WorkerHealthResponse(BaseModel):
    status: Literal["ok"]
    worker: Literal["available"]
    mode: Literal["api_placeholder"]
