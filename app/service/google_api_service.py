from datetime import datetime

from aiogoogle.client import Aiogoogle

from app.core.constants import (FORMAT, PERMISSIONS_BODY, SPREADSHEET_BODY,
                                TABLE_VALUES, UPDATE_BODY)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:

    now_date_time = datetime.now().strftime(FORMAT)
    TABLE_VALUES[0][1] = now_date_time

    service = await wrapper_services.discover('sheets', 'v4')

    for project in projects:
        new_row = [str(project['name']), str(project['collection_period']),
                   str(project['description'])]
        TABLE_VALUES.append(new_row)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=UPDATE_BODY
        )
    )
