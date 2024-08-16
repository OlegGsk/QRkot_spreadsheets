from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LEN_NAME_PROJECT
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(length=MAX_LEN_NAME_PROJECT),
                  unique=True, nullable=False)
    description = Column(Text, nullable=False)
