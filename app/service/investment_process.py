from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from app.service.utils import check_crud, update_project_or_donation


async def process_investing(
        object_invest: Union[Donation, CharityProject],
        crud: CRUDBase,
        session: AsyncSession
):
    """
    Обработка инвестиций. В зависимости от типа объекта
    (Donation, CharityProject) заполняются поля invested_amount и
    fully_invested , close_date. После этого происходит обновление объекта.
    """
    object_invest_diff = (object_invest.full_amount -
                          object_invest.invested_amount)
    check_objects = await crud.get_not_closed_objects(session=session)

    for check_obj in check_objects:
        check_obj_diff = (check_obj.full_amount -
                          check_obj.invested_amount)
        min_diff = min(object_invest_diff, check_obj_diff)

        object_invest.invested_amount += min_diff
        check_obj.invested_amount += min_diff

        closing_object_invest = (object_invest.invested_amount ==
                                 object_invest.full_amount)
        closing_check_obj = (check_obj.invested_amount ==
                             check_obj.full_amount)

        await update_project_or_donation(
            object_invest=object_invest,
            session=session,
            closing=closing_object_invest
        )

        await update_project_or_donation(
            object_invest=check_obj,
            session=session,
            closing=closing_check_obj
        )
        if closing_object_invest:
            break

    await session.commit()
    await session.refresh(object_invest)


async def start_investment_process(
        object_invest: Union[Donation, CharityProject],
        session: AsyncSession):
    crud = check_crud(object_invest=object_invest)
    await process_investing(
        object_invest=object_invest,
        crud=crud,
        session=session
    )
