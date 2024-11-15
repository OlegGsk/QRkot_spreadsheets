from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    async def get_donations_by_user_id(
            self,
            user_id: int,
            session: AsyncSession
    ) -> Optional[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
