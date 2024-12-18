import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr
from pydantic import EmailStr

from app.domain.common.enums import UserStatuses
from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment


class User(APIModel):
    id: UUID
    firstname: str
    lastname: str
    email: EmailStr
    description: str | None = None
    status: UserStatuses
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class Staff(APIModel):
    id: UUID
    firstname: str | None = None
    lastname: str | None = None
    qualification: str | None = None
    post: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    link_to_vk: str | None = None
    status: UserStatuses | None = None
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class StaffInternal(APIModel):
    id: UUID
    firstname: str | None = None
    lastname: str | None = None
    qualification: str | None = None
    post: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    link_to_vk: str | None = None
    status: UserStatuses | None = None
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class ProjectAttachment(APIModel):
    id: UUID
    project_id: UUID | None = None
    attachment_id: UUID | None = None
    created_at: datetime


class StaffDetails(Staff):
    avatar_attachment: Attachment | None = None


class ProjectAttachmentDetails(Attachment):
    attachment: Attachment | None = None


class UserDetails(User):
    avatar_attachment: Attachment | None = None


class UserDetailsFull(UserDetails):
    permissions: set[str] | None = None


class UserCredentials(APIModel):
    email: str
    password: str


class UserCredentialsRegist(APIModel):
    firstname: str
    lastname: str
    email: str
    password: str


class UserCreate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None


class StaffCreate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    qualification: str | None = None
    post: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    link_to_vk: str | None = None
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None


class StaffCreateFull(StaffCreate):
    status: UserStatuses


class UserCreateFull(UserCreate):
    status: UserStatuses


class UserPartialUpdate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None
    status: str | None = None


class UserPartialUpdateFull(UserPartialUpdate):
    password_hash: str | None = None


class UserInternal(APIModel):
    id: UUID
    firstname: str
    lastname: str
    qualification: str | None = None
    post: str | None = None
    email: EmailStr
    description: str | None = None
    link_to_vk: str | None = None
    password_hash: str
    permissions: set[str] | None = None
    avatar_attachment_id: UUID | None = None
    avatar_attachment: Attachment | None = None
    status: UserStatuses
    created_at: datetime


class UserSorts(enum.StrEnum):
    id = enum.auto()
    firstname = enum.auto()
    email = enum.auto()
    status = enum.auto()
    created_at = enum.auto()


class StaffSorts(enum.StrEnum):
    id = enum.auto()
    firstname = enum.auto()
    email = enum.auto()
    status = enum.auto()
    created_at = enum.auto()
    post = enum.auto()


class EmailForCode(APIModel):
    email: str | None = None


class VerificationCode(APIModel):
    email: str
    code: int


class UpdatePasswordConfirm(APIModel):
    email: str | None = None
    code: str | None = None
    password: str | None = None


class UserProfilePartialUpdate(APIModel):
    firstname: str | None = None
    password: str | None = None


class PasswordResetCode(APIModel):
    user_id: UUID | None = None
    staff_id: UUID | None = None
    code: str


class EmailVerificationCode(APIModel):
    email: str
    code: int


class PasswordResetCodePartialUpdate(APIModel):
    code: str | None = None


@dataclass
class UserListRequestSchema:
    pagination: pg.PaginationCallable[User] | None = None
    sorting: sr.SortingData[UserSorts] | None = None


@dataclass
class StaffListRequestSchema:
    pagination: pg.PaginationCallable[Staff] | None = None
    sorting: sr.SortingData[StaffSorts] | None = None


@dataclass
class UserWhere:
    id: UUID | None = None
    firstname: str | None = None
    email: str | None = None


@dataclass
class PasswordResetCodeWhere:
    id: int | None = None
    user_id: UUID | None = None
    staff_id: UUID | None = None
    code: str | None = None
