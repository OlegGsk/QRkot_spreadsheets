from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra

from app.schemas.base import PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationShortDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
