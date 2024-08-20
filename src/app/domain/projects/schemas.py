import enum
from dataclasses import dataclass
from datetime import datetime
from typing import IO
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment


class Project(APIModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    description: str
    likes: int
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class ProjectCreate(APIModel):
    name: str
    start_date: datetime
    end_date: datetime
    description: str


class ProjectPartialUpdate(APIModel):
    avatar_attachment_id: UUID | None = None


class ProjectDetailsFull(Project):
    avatar_attachment: Attachment | None = None


class Like(APIModel):
    project_id: int


class LikeTheProject(APIModel):
    project_id: int
    user_id: UUID | None = None
    staff_id: UUID | None = None


class ProjectSorts(enum.StrEnum):
    id = enum.auto()
    name = enum.auto()
    start_date: datetime
    end_date: datetime
    description = enum.auto()
    likes = enum.auto()
    created_at = enum.auto()


@dataclass
class ProjectListRequestSchema:
    pagination: pg.PaginationCallable[ProjectDetailsFull] | None = None
    sorting: sr.SortingData[ProjectSorts] | None = None


@dataclass
class ProjectWhere:
    id: int | None = None
