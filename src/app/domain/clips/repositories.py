from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from sqlalchemy import ColumnElement, and_, select, insert, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models
from app.domain.common.schemas import IdContainerTables
from app.domain.clips import schemas


class ClipRepository(CrudRepositoryMixin[models.Clip]):
    load_options: list[ExecutableOption] = [
        selectinload(models.Clip.clip_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Clip
        self.transaction = transaction

    async def create_clip(self, payload: schemas.ClipCreate) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))

    async def get_clip(
            self,
            pagination: PaginationCallable[schemas.Clip] | None = None,
            sorting: SortingData[schemas.ClipSorts] | None = None,
    ) -> Paginated[schemas.Clip]:
        return await self._get_list(
            schemas.Clip,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def partial_update_clip(self, clip_id: UUID, payload: schemas.ClipPartialUpdate) -> None:
        return await self._partial_update(clip_id, payload)

    async def get_clip_by_filter_or_none(self, where: schemas.ClipWhere) -> schemas.ClipDetailsFull | None:
        return await self._get_or_none(
            schemas.ClipDetailsFull,
            condition=await self._format_filters(where),
            options=self.load_options,
        )

    async def _format_filters(self, where: schemas.ClipWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.Clip.id == where.id)

        return and_(*filters)

    async def update_clip_likes(self, clip_id: int, clip_likes_count: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                update(models.Clip)
                .where(models.Clip.id == clip_id)
                .values(likes=clip_likes_count)
            )
            await session.execute(stmt)
            await session.commit()


class LikeClipRepository(CrudRepositoryMixin[models.ClipLike]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.ClipLike
        self.transaction = transaction

    async def create_like_clip(self, payload: schemas.LikeTheClip) -> IdContainerTables:
        async with self.transaction.use() as session:
            try:
                like_query = select(models.ClipLike).where(
                    (models.ClipLike.user_id == payload.user_id) &
                    (models.ClipLike.clip_id == payload.clip_id)
                )
                like_exists = await session.execute(like_query)
                existing_like = like_exists.scalar_one_or_none()

                if existing_like:
                    return

                staff_query = select(models.Staff).where(models.Staff.id == payload.user_id)
                staff_exists = await session.execute(staff_query)

                if staff_exists.first():
                    stmt = insert(models.ClipLike).values(
                        {
                            "staff_id": payload.user_id,
                            "clip_id": payload.clip_id,
                        }
                    )
                else:
                    stmt = insert(models.ClipLike).values(
                        {
                            "user_id": payload.user_id,
                            "clip_id": payload.clip_id,
                        }
                    )

                await session.execute(stmt)

            except Exception as e:
                print(f"Error creating like info: {e}")

    async def delete_like_clip(self, clip_id: int, user_id: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                delete(models.ClipLike)
                .where(
                    and_(
                        models.ClipLike.clip_id == clip_id,
                        models.ClipLike.user_id == user_id
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

    async def check_like_exists(self, clip_id: int, user_id: int) -> bool:
        async with self.transaction.use() as session:
            stmt = select(models.ClipLike).where(
                and_(
                    models.ClipLike.clip_id == clip_id,
                    models.ClipLike.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            return result.first() is not None
