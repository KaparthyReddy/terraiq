from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SensorReadingCreate(BaseModel):
    field_id: str
    sensor_id: str
    ph: Optional[float] = None
    moisture_pct: Optional[float] = None
    temperature_c: Optional[float] = None
    nitrogen_ppm: Optional[float] = None
    phosphorus_ppm: Optional[float] = None
    potassium_ppm: Optional[float] = None
    organic_matter_pct: Optional[float] = None
    electrical_conductivity: Optional[float] = None
    spectral_signature: Optional[str] = None


class SensorReadingOut(BaseModel):
    id: str
    field_id: str
    sensor_id: str
    ph: Optional[float]
    moisture_pct: Optional[float]
    temperature_c: Optional[float]
    nitrogen_ppm: Optional[float]
    phosphorus_ppm: Optional[float]
    potassium_ppm: Optional[float]
    organic_matter_pct: Optional[float]
    electrical_conductivity: Optional[float]
    recorded_at: datetime

    model_config = {"from_attributes": True}
