import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment
from app.domain.users.core.schemas import Staff, StaffDetails, ProjectAttachmentDetails


class Project(APIModel):
    id: UUID
    name: str
    start_date: datetime
    end_date: datetime
    description: str
    participants: int
    lessons: int
    likes: int
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class ProjectCreate(APIModel):
    name: str
    start_date: datetime
    end_date: datetime
    description: str
    participants: int
    lessons: int


class ProjectDelete(APIModel):
    id: UUID


class AddEmployees(APIModel):
    project_id: UUID
    staff_id: UUID


class ProjectPartialUpdate(APIModel):
    avatar_attachment_id: UUID | None = None


class ProjectDetailsFull(Project):
    avatar_attachment: Attachment | None = None


class ProjectStaffShort(APIModel):
    id: UUID
    staff_id: UUID
    first_name: str | None = None
    last_name: str | None = None
    post: str | None = None
    avatar_attachment_id: UUID | None = None


class ProjectAttachment(APIModel):
    project_id: UUID | None = None
    attachment_id: UUID | None = None


class ProjectAttachmentDetailsShort(APIModel):
    attachment: Attachment | None = None


class ProjectStaffDetailsShort(APIModel):
    staff: Staff | None = None


class Like(APIModel):
    project_id: UUID | None = None
    news_id: UUID | None = None
    clip_id: int | None = None


class LikeTheProject(APIModel):
    project_id: UUID
    user_id: UUID | None = None
    staff_id: UUID | None = None


class ProjectSorts(enum.StrEnum):
    id = enum.auto()
    name = enum.auto()
    start_date: datetime
    end_date: datetime
    description = enum.auto()
    participants = enum.auto()
    lessons = enum.auto()
    likes = enum.auto()
    created_at = enum.auto()


class ProjectStaffSorts(enum.StrEnum):
    id = enum.auto()
    first_name = enum.auto()
    last_name: enum.auto()
    project_id = enum.auto()
    created_at = enum.auto()


class ProjectAttachmentSorts(enum.StrEnum):
    id = enum.auto()
    project_id = enum.auto()
    created_at = enum.auto()


@dataclass
class ProjectListRequestSchema:
    pagination: pg.PaginationCallable[ProjectDetailsFull] | None = None
    sorting: sr.SortingData[ProjectSorts] | None = None


@dataclass
class ProjectStaffListRequestSchema:
    project_id: UUID
    pagination: pg.PaginationCallable[StaffDetails] | None = None
    sorting: sr.SortingData[ProjectStaffSorts] | None = None


@dataclass
class ProjectAttachmentListRequestSchema:
    project_id: UUID
    pagination: pg.PaginationCallable[ProjectAttachmentDetails] | None = None
    sorting: sr.SortingData[ProjectAttachmentSorts] | None = None


@dataclass
class ProjectWhere:
    id: UUID | None = None
