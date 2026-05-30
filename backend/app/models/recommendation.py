import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    field_id: Mapped[str] = mapped_column(String, ForeignKey("fields.id"), nullable=False, index=True)

    # What triggered this recommendation
    trigger: Mapped[str] = mapped_column(String, nullable=False)  # "sensor" | "satellite" | "scheduled"

    # ML model outputs
    microbiome_health_score: Mapped[float] = mapped_column(Float, nullable=True)  # 0.0 - 1.0
    predicted_yield_impact_pct: Mapped[float] = mapped_column(Float, nullable=True)

    # Structured action items from the recommendation engine
    actions: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)

    # Human-readable summary
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # NDVI snapshot at time of recommendation
    ndvi_value: Mapped[float] = mapped_column(Float, nullable=True)

    confidence: Mapped[float] = mapped_column(Float, nullable=True)  # 0.0 - 1.0
    status: Mapped[str] = mapped_column(String, default="pending")  # pending | applied | dismissed

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    field: Mapped["Field"] = relationship("Field", back_populates="recommendations")
