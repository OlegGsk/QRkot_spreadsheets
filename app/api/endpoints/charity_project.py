from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_full_amount,
                                check_project_invested_amount_or_close_date,
                                check_unique_project_name)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.service.investment_process import start_investment_process

router = APIRouter()


@router.post('/', response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)], )
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_unique_project_name(project_name=charity_project.name,
                                    session=session)

    project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session
    )

    await start_investment_process(
        object_invest=project,
        session=session
    )
    return project


@router.get('/', response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_project_crud.get_multi(session=session)
    return projects


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)], )
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )
    await check_project_invested_amount_or_close_date(
        invested_amount=project.invested_amount,
        close_date=project.close_date,
        message='Нельзя удалить закрытый проект или проект с вложениями'
    )

    project = await charity_project_crud.remove(
        db_obj=project,
        session=session
    )
    return project


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              response_model_exclude_none=True,
              dependencies=[Depends(current_superuser)], )
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(
        project_id=project_id,
        session=session
    )
    if obj_in.name is not None:
        await check_unique_project_name(project_name=obj_in.name,
                                        session=session,
                                        project_id=project_id)
    if obj_in.full_amount is not None:
        await check_full_amount(
            full_amount=obj_in.full_amount,
            invested_amount=project.invested_amount
        )

    await check_project_invested_amount_or_close_date(
        close_date=project.close_date,
        message='Нельзя обновить закрытый проект'
    )
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )

    await start_investment_process(
        object_invest=project,
        session=session
    )

    return project
