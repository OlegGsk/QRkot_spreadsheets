from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationShortDB
from app.service.investment_process import start_investment_process

router = APIRouter()


@router.post('/', response_model=DonationShortDB,
             dependencies=[Depends(current_user)])
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user
    )

    await start_investment_process(object_invest=donation,
                                   session=session)
    return donation


@router.get('/',
            dependencies=[Depends(current_superuser)],
            response_model=list[DonationDB])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session=session)
    return donations


@router.get('/my',
            response_model=list[DonationShortDB], )
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_donations_by_user_id(
        user_id=user.id,
        session=session
    )
    return donations
