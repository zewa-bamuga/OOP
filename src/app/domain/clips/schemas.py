import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment


class Clip(APIModel):
    id: int
    name: str
    date: datetime
    description: str
    likes: int
    clip_attachment_id: UUID | None = None
    created_at: datetime


class ClipCreate(APIModel):
    name: str
    date: datetime
    description: str


class ClipDetailsFull(Clip):
    clip_attachment: Attachment | None = None


class ClipPartialUpdate(APIModel):
    clip_attachment_id: UUID | None = None


class ClipDelete(APIModel):
    clip_id: int
    user_id: UUID | None = None


class LikeTheClip(APIModel):
    clip_id: int
    user_id: UUID | None = None
    staff_id: UUID | None = None


class ClipSorts(enum.StrEnum):
    id = enum.auto()
    name = enum.auto()
    date = enum.auto()
    description = enum.auto()
    likes = enum.auto()
    created_at = enum.auto()


@dataclass
class ClipListRequestSchema:
    pagination: pg.PaginationCallable[ClipDetailsFull] | None = None
    sorting: sr.SortingData[ClipSorts] | None = None


@dataclass
class ClipWhere:
    id: int | None = None
