from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.field import Field
from app.models.user import User
from app.schemas.field import FieldCreate, FieldUpdate, FieldOut

router = APIRouter()


@router.get("/", response_model=List[FieldOut])
async def list_fields(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Field).where(Field.owner_id == current_user.id))
    return result.scalars().all()


@router.post("/", response_model=FieldOut, status_code=status.HTTP_201_CREATED)
async def create_field(
    payload: FieldCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    field = Field(**payload.model_dump(), owner_id=current_user.id)
    db.add(field)
    await db.commit()
    await db.refresh(field)
    return field


@router.get("/{field_id}", response_model=FieldOut)
async def get_field(
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
    return field


@router.patch("/{field_id}", response_model=FieldOut)
async def update_field(
    field_id: str,
    payload: FieldUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Field).where(Field.id == field_id, Field.owner_id == current_user.id)
    )
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(field, key, value)

    await db.commit()
    await db.refresh(field)
    return field


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(
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
    await db.delete(field)
    await db.commit()
