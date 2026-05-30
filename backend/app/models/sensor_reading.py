import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    field_id: Mapped[str] = mapped_column(String, ForeignKey("fields.id"), nullable=False, index=True)
    sensor_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    # Core soil metrics
    ph: Mapped[float] = mapped_column(Float, nullable=True)
    moisture_pct: Mapped[float] = mapped_column(Float, nullable=True)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=True)
    nitrogen_ppm: Mapped[float] = mapped_column(Float, nullable=True)
    phosphorus_ppm: Mapped[float] = mapped_column(Float, nullable=True)
    potassium_ppm: Mapped[float] = mapped_column(Float, nullable=True)
    organic_matter_pct: Mapped[float] = mapped_column(Float, nullable=True)
    electrical_conductivity: Mapped[float] = mapped_column(Float, nullable=True)

    # Spectral data from NIR sensor (serialized as comma-separated floats)
    spectral_signature: Mapped[str] = mapped_column(String, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

    field: Mapped["Field"] = relationship("Field", back_populates="sensor_readings")
