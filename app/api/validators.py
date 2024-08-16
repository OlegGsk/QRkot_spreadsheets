from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_unique_project_name(
        *,
        project_name: str,
        project_id: Optional[int] = None,
        session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_project_id_by_name(
        project_name=project_name,
        project_id=project_id,
        session=session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not unique name', )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден',
        )
    return project


async def check_project_invested_amount_or_close_date(
        *,
        invested_amount: Optional[int] = None,
        close_date: Optional[datetime],
        message: str
) -> None:
    if invested_amount is not None:
        if close_date is not None or invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=message,
            )
    if close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=message,
        )


async def check_full_amount(
        full_amount: int,
        invested_amount: int,
) -> None:
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Запрещено устанавливать требуемую сумму меньше внесённой'
        )
