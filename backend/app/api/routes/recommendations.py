from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api.deps import get_db, get_current_user
from app.models.field import Field
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.recommendation import RecommendationOut, RecommendationStatusUpdate

router = APIRouter()


@router.get("/{field_id}", response_model=List[RecommendationOut])
async def list_recommendations(
    field_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Field).where(Field.id == field_id, Field.owner_id == current_user.id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Field not found")

    result = await db.execute(
        select(Recommendation)
        .where(Recommendation.field_id == field_id)
        .order_by(desc(Recommendation.created_at))
    )
    return result.scalars().all()


@router.patch("/{recommendation_id}/status", response_model=RecommendationOut)
async def update_status(
    recommendation_id: str,
    payload: RecommendationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Recommendation).where(Recommendation.id == recommendation_id)
    )
    rec = result.scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    if payload.status not in ("applied", "dismissed"):
        raise HTTPException(status_code=400, detail="Invalid status")

    rec.status = payload.status
    await db.commit()
    await db.refresh(rec)
    return rec
