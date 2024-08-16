from datetime import datetime
from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation
from app.schemas.base import DonationProjectInvestmentUpdate


def check_crud(
        object_invest: Union[Donation, CharityProject]):
    if isinstance(object_invest, Donation):
        crud = charity_project_crud
    else:
        crud = donation_crud
    return crud


async def update_project_or_donation(
        object_invest: Union[Donation, CharityProject],
        session: AsyncSession,
        closing: Optional[bool] = False,
):
    crud = check_crud(object_invest)

    if closing:
        object_invest.fully_invested = True
        object_invest.close_date = datetime.now()
    await crud.update(
        obj_in=DonationProjectInvestmentUpdate(
            invested_amount=object_invest.invested_amount,
            fully_invested=object_invest.fully_invested,
            close_date=object_invest.close_date),
        session=session,
        db_obj=object_invest,
        invest=True
    )
