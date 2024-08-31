from uuid import UUID

import sqlalchemy as sa
from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from sqlalchemy import ColumnElement, and_, select, insert, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models, enums
from app.domain.common.schemas import IdContainer, IdContainerTables
from app.domain.projects import schemas


class NewsRepository(CrudRepositoryMixin[models.News]):
    load_options: list[ExecutableOption] = [
        selectinload(models.News.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.News
        self.transaction = transaction

    async def create_news(self, payload: schemas.ProjectCreate) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))
