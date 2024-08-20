from typing import Union

from aiogoogle.client import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.service.google_api_service import (get_all_files, get_sheet_by_id,
                                            remove_sheet_by_id,
                                            set_user_permissions,
                                            spreadsheets_create,
                                            spreadsheets_update_value)

router = APIRouter()


@router.post('/',
             dependencies=[Depends(current_superuser)],
             response_model=list[dict])
async def get_projects(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)

    spreadsheet_id = await spreadsheets_create(wrapper_services)

    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    projects,
                                    wrapper_services)
    return projects


@router.get('/all_files',
            response_model=list[dict[str, str]])
async def get_files(
        wrapper_services: Aiogoogle = Depends(get_service)
):
    return await get_all_files(wrapper_services)


@router.get('/get_sheet',
            response_model=Union[list[list[str]], str])
async def get_sheet_by_id_api(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle = Depends(get_service)
):
    return await get_sheet_by_id(spreadsheet_id, wrapper_services)


@router.delete('/remove_sheet')
async def remove_sheet_by_id_api(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle = Depends(get_service)
):
    await remove_sheet_by_id(spreadsheet_id, wrapper_services)
    # return f'{spreadsheet_id} удален из Google Drive'
