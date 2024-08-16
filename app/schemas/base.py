from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

PositiveInt = Annotated[int, Field(gt=0)]


class DonationProjectInvestmentUpdate(BaseModel):
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    close_date: Optional[datetime]
