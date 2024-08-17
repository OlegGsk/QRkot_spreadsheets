from datetime import datetime

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

MIN_LEN_PASSWORD = 3

MAX_LEN_NAME_PROJECT = 100

MAX_LEN_DESCRIPTION_PROJECT = 1000

MIN_LEN_DESCRIPTION_PROJECT = 1

SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт о закрытых проектах',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]}

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}

NOW_DATE_TIME = datetime.now().strftime(FORMAT)

TABLE_VALUES = [
    ['Отчёт от', NOW_DATE_TIME],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']]

UPDATE_BODY = {
    'majorDimension': 'ROWS',
    'values': TABLE_VALUES}
