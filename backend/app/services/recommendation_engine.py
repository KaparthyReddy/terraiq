import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sensor_reading import SensorReading
from app.models.recommendation import Recommendation
from app.models.field import Field
from app.services.satellite_fetch import fetch_ndvi

log = structlog.get_logger()

# Threshold rules that trigger an immediate recommendation
ALERT_THRESHOLDS = {
    "ph":              (5.0, 8.5),    # (min, max)
    "moisture_pct":    (15.0, 80.0),
    "nitrogen_ppm":    (10.0, 300.0),
    "phosphorus_ppm":  (5.0, 150.0),
    "potassium_ppm":   (50.0, 400.0),
}


def _build_actions(reading: SensorReading) -> list[dict]:
    actions = []

    if reading.ph is not None:
        if reading.ph < 5.5:
            actions.append({
                "type": "apply_amendment",
                "input": "Agricultural lime (CaCO3)",
                "quantity_kg_ha": round((6.5 - reading.ph) * 1200, 1),
                "timing": "Pre-season, incorporate to 15cm",
                "priority": "high",
            })
        elif reading.ph > 7.8:
            actions.append({
                "type": "apply_amendment",
                "input": "Elemental sulfur",
                "quantity_kg_ha": round((reading.ph - 6.8) * 300, 1),
                "timing": "Apply 3 months before planting",
                "priority": "medium",
            })

    if reading.nitrogen_ppm is not None and reading.nitrogen_ppm < 20:
        actions.append({
            "type": "fertilize",
            "input": "Urea 46-0-0",
            "quantity_kg_ha": round((40 - reading.nitrogen_ppm) * 2.5, 1),
            "timing": "Split application: 50% pre-plant, 50% at tillering",
            "priority": "high",
        })

    if reading.phosphorus_ppm is not None and reading.phosphorus_ppm < 15:
        actions.append({
            "type": "fertilize",
            "input": "DAP 18-46-0",
            "quantity_kg_ha": round((25 - reading.phosphorus_ppm) * 3.0, 1),
            "timing": "Band-apply at planting",
            "priority": "medium",
        })

    if reading.moisture_pct is not None and reading.moisture_pct < 20:
        actions.append({
            "type": "irrigate",
            "input": "Drip irrigation",
            "quantity_kg_ha": None,
            "timing": "Immediate — deficit stress detected",
            "priority": "high",
        })

    return actions


def _health_score(reading: SensorReading) -> float:
    """Heuristic microbiome health score 0–1 based on sensor readings."""
    score = 1.0
    if reading.ph is not None:
        ph_dev = abs(reading.ph - 6.5) / 3.0
        score -= ph_dev * 0.25
    if reading.organic_matter_pct is not None:
        om_penalty = max(0, (3.0 - reading.organic_matter_pct) / 3.0)
        score -= om_penalty * 0.25
    if reading.moisture_pct is not None:
        m_dev = abs(reading.moisture_pct - 40.0) / 60.0
        score -= m_dev * 0.2
    return round(max(0.0, min(1.0, score)), 3)


def _is_anomalous(reading: SensorReading) -> bool:
    for field, (lo, hi) in ALERT_THRESHOLDS.items():
        val = getattr(reading, field, None)
        if val is not None and (val < lo or val > hi):
            return True
    return False


async def maybe_trigger_recommendation(reading: SensorReading, db: AsyncSession) -> None:
    if not _is_anomalous(reading):
        return

    log.info("recommendation.triggered", field_id=reading.field_id, sensor_id=reading.sensor_id)

    field_result = await db.execute(select(Field).where(Field.id == reading.field_id))
    field = field_result.scalar_one_or_none()

    ndvi_value = None
    if field:
        try:
            ndvi_data = await fetch_ndvi(field.centroid_lat, field.centroid_lon, field.boundary)
            ndvi_value = ndvi_data.get("ndvi_mean")
        except Exception:
            pass

    actions = _build_actions(reading)
    health = _health_score(reading)

    issues = []
    if reading.ph and (reading.ph < 5.5 or reading.ph > 7.8):
        issues.append(f"pH {reading.ph:.1f} outside optimal range")
    if reading.nitrogen_ppm and reading.nitrogen_ppm < 20:
        issues.append(f"low nitrogen ({reading.nitrogen_ppm:.0f} ppm)")
    if reading.moisture_pct and reading.moisture_pct < 20:
        issues.append("soil moisture deficit")

    summary = (
        f"Sensor {reading.sensor_id} detected {', '.join(issues)}. "
        f"Microbiome health score: {health:.0%}. "
        f"{len(actions)} corrective action(s) recommended."
    )

    rec = Recommendation(
        field_id=reading.field_id,
        trigger="sensor",
        microbiome_health_score=health,
        predicted_yield_impact_pct=round((health - 0.5) * 40, 1),
        actions=actions,
        summary=summary,
        ndvi_value=ndvi_value,
        confidence=0.78,
    )
    db.add(rec)
    await db.commit()
    log.info("recommendation.saved", recommendation_id=rec.id)
