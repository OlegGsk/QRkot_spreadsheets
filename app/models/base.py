from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, func

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime,
                         default=datetime.now, server_default=func.now())
    close_date = Column(DateTime, nullable=True)
