from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api.deps import get_db, get_current_user
from app.models.field import Field
from app.models.sensor_reading import SensorReading
from app.models.user import User
from app.schemas.sensor import SensorReadingCreate, SensorReadingOut
from app.services.recommendation_engine import maybe_trigger_recommendation

router = APIRouter()


@router.post("/ingest", response_model=SensorReadingOut, status_code=201)
async def ingest_reading(
    payload: SensorReadingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify field ownership
    result = await db.execute(
        select(Field).where(Field.id == payload.field_id, Field.owner_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Field not found")

    reading = SensorReading(**payload.model_dump())
    db.add(reading)
    await db.commit()
    await db.refresh(reading)

    # Async trigger recommendation if thresholds breached
    await maybe_trigger_recommendation(reading, db)

    return reading


@router.get("/{field_id}/latest", response_model=SensorReadingOut)
async def latest_reading(
    field_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.field_id == field_id)
        .order_by(desc(SensorReading.recorded_at))
        .limit(1)
    )
    reading = result.scalar_one_or_none()
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found")
    return reading


@router.get("/{field_id}/history", response_model=List[SensorReadingOut])
async def reading_history(
    field_id: str,
    limit: int = Query(default=100, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.field_id == field_id)
        .order_by(desc(SensorReading.recorded_at))
        .limit(limit)
    )
    return result.scalars().all()
