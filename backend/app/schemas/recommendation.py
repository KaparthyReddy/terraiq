from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ActionItem(BaseModel):
    type: str          # "fertilize" | "irrigate" | "till" | "apply_amendment"
    input: str         # e.g. "Urea 46-0-0"
    quantity_kg_ha: Optional[float] = None
    timing: Optional[str] = None
    priority: str = "medium"  # "high" | "medium" | "low"


class RecommendationOut(BaseModel):
    id: str
    field_id: str
    trigger: str
    microbiome_health_score: Optional[float]
    predicted_yield_impact_pct: Optional[float]
    actions: List[ActionItem]
    summary: str
    ndvi_value: Optional[float]
    confidence: Optional[float]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RecommendationStatusUpdate(BaseModel):
    status: str  # "applied" | "dismissed"
