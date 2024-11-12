from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from sqlalchemy import ColumnElement, and_, select, insert, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models
from app.domain.common.schemas import IdContainerTables, IdContainer
from app.domain.news import schemas


class NewsRepository(CrudRepositoryMixin[models.News]):
    load_options: list[ExecutableOption] = [
        selectinload(models.News.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.News
        self.transaction = transaction

    async def create_news(self, payload: schemas.NewsCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_news(
            self,
            pagination: PaginationCallable[schemas.News] | None = None,
            sorting: SortingData[schemas.NewsSorts] | None = None,
    ) -> Paginated[schemas.News]:
        return await self._get_list(
            schemas.News,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def update_news_likes(self, news_id: UUID, new_likes_count: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                update(models.News)
                .where(models.News.id == news_id)
                .values(likes=new_likes_count)
            )
            await session.execute(stmt)
            await session.commit()

    async def update_news_reminder(self, news_id: UUID, new_reminder_count: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                update(models.News)
                .where(models.News.id == news_id)
                .values(likes=new_reminder_count)
            )
            await session.execute(stmt)
            await session.commit()

    async def partial_update_news(self, news_id: UUID, payload: schemas.NewsPartialUpdate) -> None:
        return await self._partial_update(news_id, payload)

    async def get_news_by_filter_or_none(self, where: schemas.NewsWhere) -> schemas.NewsDetailsFull | None:
        return await self._get_or_none(
            schemas.NewsDetailsFull,
            condition=await self._format_filters(where),
            options=self.load_options,
        )

    async def _format_filters(self, where: schemas.NewsWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.News.id == where.id)

        return and_(*filters)


class ReminderNewsRepository(CrudRepositoryMixin[models.NewsReminder]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.NewsReminder
        self.transaction = transaction

    async def create_reminder(self, payload: schemas.ReminderCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def create_task_id(self, news_id: UUID, payload: schemas.TaskIdCreate) -> None:
        print("Проискходит запись task_id в таблицу")
        return await self._partial_update(news_id, payload)


class LikeNewsRepository(CrudRepositoryMixin[models.NewsLike]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.NewsLike
        self.transaction = transaction

    async def create_like_news(self, payload: schemas.LikeTheNews) -> IdContainer:
        async with self.transaction.use() as session:
            try:
                like_query = select(models.NewsLike).where(
                    (models.NewsLike.user_id == payload.user_id) &
                    (models.NewsLike.news_id == payload.news_id)
                )
                like_exists = await session.execute(like_query)
                existing_like = like_exists.scalar_one_or_none()

                if existing_like:
                    delete_stmt = delete(models.NewsLike).where(
                        (models.NewsLike.user_id == payload.user_id) &
                        (models.NewsLike.news_id == payload.news_id)
                    )
                    await session.execute(delete_stmt)
                else:
                    staff_query = select(models.Staff).where(models.Staff.id == payload.user_id)
                    staff_exists = await session.execute(staff_query)

                    if staff_exists.first():
                        stmt = insert(models.NewsLike).values(
                            {
                                "staff_id": payload.user_id,
                                "news_id": payload.news_id,
                            }
                        )
                    else:
                        stmt = insert(models.NewsLike).values(
                            {
                                "user_id": payload.user_id,
                                "news_id": payload.news_id,
                            }
                        )

                    await session.execute(stmt)

            except Exception as e:
                print(f"Error creating like info: {e}")

    async def delete_like_news(self, news_id: int, user_id: int) -> None:
        async with self.transaction.use() as session:
            stmt = (
                delete(models.NewsLike)
                .where(
                    and_(
                        models.NewsLike.news_id == news_id,
                        models.NewsLike.user_id == user_id
                    )
                )
            )
            await session.execute(stmt)
            await session.commit()

    async def check_like_exists(self, news_id: int, user_id: int) -> bool:
        async with self.transaction.use() as session:
            stmt = select(models.NewsLike).where(
                and_(
                    models.NewsLike.news_id == news_id,
                    models.NewsLike.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            return result.first() is not None
