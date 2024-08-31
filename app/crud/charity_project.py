from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.core.constants import FORMAT

class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            *,
            project_name: str,
            project_id: Optional[int] = None,
            session: AsyncSession,
    ) -> Optional[int]:
        select_stmt = select(CharityProject.id).where(
            CharityProject.name == project_name
        )
        if project_id:
            select_stmt = select_stmt.where(
                CharityProject.id != project_id
            )
        project = await session.execute(select_stmt)

        project_id = project.scalars().first()
        return project_id

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        projects = await session.execute(
            select([self.model.name,
                    (self.model.close_date - self.model.create_date
                     ).label("collection_period"),
                    self.model.description]).where(
                self.model.fully_invested
            ).order_by(
                'collection_period'
            )
        )
        projects = projects.all()

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
