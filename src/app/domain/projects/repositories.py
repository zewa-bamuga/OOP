from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from sqlalchemy import ColumnElement, and_, select, insert, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models
from app.domain.common.schemas import IdContainer
from app.domain.projects import schemas


class ProjectAttachmentRepository(CrudRepositoryMixin[models.ProjectAttachment]):
    load_options: list[ExecutableOption] = [
        selectinload(models.ProjectAttachment.attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.ProjectAttachment
        self.transaction = transaction

    async def create_project_attachment(self, payload: schemas.ProjectAttachment) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_project_attachment(
            self,
            project_id: UUID,
            pagination: PaginationCallable[schemas.ProjectAttachmentDetailsShort] | None = None,
            sorting: SortingData[schemas.ProjectAttachmentSorts] | None = None,
    ) -> Paginated[schemas.ProjectAttachmentDetailsShort]:
        condition = self.model.project_id == project_id
        return await self._get_list(
            schema=schemas.ProjectAttachmentDetailsShort,
            pagination=pagination,
            sorting=sorting,
            condition=condition,
            options=self.load_options,
        )


class ProjectRepository(CrudRepositoryMixin[models.Project]):
    load_options: list[ExecutableOption] = [
        selectinload(models.Project.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Project
        self.transaction = transaction

    async def create_project(self, payload: schemas.ProjectCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def delete_project(self, payload: schemas.ProjectDelete) -> None:
        async with self.transaction.use() as session:
            stmt = (
                delete(models.Project)
                .where(
                    and_(
                        models.Project.id == payload.id,
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

    async def partial_update_project(self, project_id: UUID, payload: schemas.ProjectPartialUpdate) -> None:
        return await self._partial_update(project_id, payload)

    async def get_project(
            self,
            pagination: PaginationCallable[schemas.Project] | None = None,
            sorting: SortingData[schemas.ProjectSorts] | None = None,
    ) -> Paginated[schemas.Project]:
        return await self._get_list(
            schemas.Project,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def get_project_by_filter_or_none(self, where: schemas.ProjectWhere) -> schemas.ProjectDetailsFull | None:
        return await self._get_or_none(
            schemas.ProjectDetailsFull,
            condition=await self._format_filters(where),
            options=self.load_options,
        )

    async def update_project_likes(self, project_id: int, new_likes_count: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                update(models.Project)
                .where(models.Project.id == project_id)
                .values(likes=new_likes_count)
            )
            await session.execute(stmt)
            await session.commit()

    async def _format_filters(self, where: schemas.ProjectWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.Project.id == where.id)

        return and_(*filters)


class ProjectStaffRepository(CrudRepositoryMixin[models.ProjectStaff]):
    load_options: list[ExecutableOption] = [
        selectinload(models.ProjectStaff.staff),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.ProjectStaff
        self.transaction = transaction

    async def create_add_staff_project(self, payload: schemas.AddEmployees) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_project_staff(
            self,
            project_id: UUID,
            pagination: PaginationCallable[schemas.ProjectStaffDetailsShort] | None = None,
            sorting: SortingData[schemas.ProjectStaffSorts] | None = None,
    ) -> Paginated[schemas.ProjectStaffDetailsShort]:
        condition = self.model.project_id == project_id
        return await self._get_list(
            schema=schemas.ProjectStaffDetailsShort,
            pagination=pagination,
            sorting=sorting,
            condition=condition,
            options=self.load_options,
        )


class LikeTheProjectRepository(CrudRepositoryMixin[models.ProjectLike]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.ProjectLike
        self.transaction = transaction

    async def create_like_project(self, payload: schemas.LikeTheProject) -> IdContainer:
        async with self.transaction.use() as session:
            try:
                like_query = select(models.ProjectLike).where(
                    (models.ProjectLike.user_id == payload.user_id) &
                    (models.ProjectLike.project_id == payload.project_id)
                )
                like_exists = await session.execute(like_query)
                existing_like = like_exists.scalar_one_or_none()

                if existing_like:
                    delete_stmt = delete(models.ProjectLike).where(
                        (models.ProjectLike.user_id == payload.user_id) &
                        (models.ProjectLike.project_id == payload.project_id)
                    )
                    await session.execute(delete_stmt)
                else:
                    staff_query = select(models.Staff).where(models.Staff.id == payload.user_id)
                    staff_exists = await session.execute(staff_query)

                    if staff_exists.first():
                        stmt = insert(models.ProjectLike).values(
                            {
                                "staff_id": payload.user_id,
                                "project_id": payload.project_id,
                            }
                        )
                    else:
                        stmt = insert(models.ProjectLike).values(
                            {
                                "user_id": payload.user_id,
                                "project_id": payload.project_id,
                            }
                        )

                    await session.execute(stmt)

            except Exception as e:
                print(f"Error creating like info: {e}")

    async def delete_like_project(self, project_id: int, user_id: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                delete(models.ProjectLike)
                .where(
                    and_(
                        models.ProjectLike.project_id == project_id,
                        models.ProjectLike.user_id == user_id
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

    async def check_like_exists(self, project_id: int, user_id: int) -> bool:
        async with self.transaction.use() as session:
            stmt = select(models.ProjectLike).where(
                and_(
                    models.ProjectLike.project_id == project_id,
                    models.ProjectLike.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            return result.first() is not None
