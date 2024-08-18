from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.constants import (MAX_LEN_DESCRIPTION_PROJECT,
                                MAX_LEN_NAME_PROJECT,
                                MIN_LEN_DESCRIPTION_PROJECT)
from app.schemas.base import PositiveInt


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=MAX_LEN_NAME_PROJECT)
    description: str = Field(..., min_length=MIN_LEN_DESCRIPTION_PROJECT,
                             max_length=MAX_LEN_DESCRIPTION_PROJECT)

    @validator('name')
    def check_name(cls, value):
        if not value:
            raise ValueError('поле name не может быть пустым')
        return value


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
