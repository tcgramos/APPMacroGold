from datetime import datetime
from pydantic import BaseModel


class AssetSnapshot(BaseModel):
    symbol: str
    price: float
    pct_change: float
    trend: str


class MacroScore(BaseModel):
    direction: str
    score: int
    reason: str


class AlertOut(BaseModel):
    id: int
    event_type: str
    severity: str
    message: str
    confidence: int
    created_at: datetime

    class Config:
        from_attributes = True
