from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.field import Field
from app.models.user import User
from app.services.satellite_fetch import fetch_ndvi
from sqlalchemy import select

router = APIRouter()


@router.get("/{field_id}/ndvi")
async def get_ndvi(
    field_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Field).where(Field.id == field_id, Field.owner_id == current_user.id)
    )
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    ndvi_data = await fetch_ndvi(
        lat=field.centroid_lat,
        lon=field.centroid_lon,
        boundary=field.boundary,
    )
    return ndvi_data
