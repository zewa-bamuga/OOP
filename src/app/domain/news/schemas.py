import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment


class News(APIModel):
    id: int
    name: str
    date: datetime
    description: str
    likes: int
    reminder: int
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class NewsCreate(APIModel):
    name: str
    date: datetime
    description: str


class NewsDetailsFull(News):
    avatar_attachment: Attachment | None = None


class NewsPartialUpdate(APIModel):
    avatar_attachment_id: UUID | None = None


class NewsSorts(enum.StrEnum):
    id = enum.auto()
    name = enum.auto()
    date = enum.auto()
    description = enum.auto()
    likes = enum.auto()
    created_at = enum.auto()


class LikeTheNews(APIModel):
    news_id: int
    user_id: UUID | None = None
    staff_id: UUID | None = None


@dataclass
class NewsListRequestSchema:
    pagination: pg.PaginationCallable[NewsDetailsFull] | None = None
    sorting: sr.SortingData[NewsSorts] | None = None


@dataclass
class NewsWhere:
    id: int | None = None
