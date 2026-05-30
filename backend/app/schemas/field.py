from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FieldCreate(BaseModel):
    name: str
    area_hectares: float
    boundary: dict
    centroid_lat: float
    centroid_lon: float
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None


class FieldUpdate(BaseModel):
    name: Optional[str] = None
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None


class FieldOut(BaseModel):
    id: str
    name: str
    area_hectares: float
    boundary: dict
    centroid_lat: float
    centroid_lon: float
    crop_type: Optional[str]
    soil_type: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
