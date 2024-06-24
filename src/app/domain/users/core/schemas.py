import enum
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import EmailStr

from app.domain.common.enums import UserStatuses
from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment
from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr


class User(APIModel):
    id: UUID
    username: str
    email: str
    status: UserStatuses
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class UserDetails(User):
    avatar_attachment: Attachment | None = None


class UserDetailsFull(UserDetails):
    permissions: set[str] | None = None


class UserCredentials(APIModel):
    username: str
    email: str
    password: str


class UserCreate(APIModel):
    username: str
    email: EmailStr
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None


class UserCreateFull(UserCreate):
    status: UserStatuses


class UserPartialUpdate(APIModel):
    username: str | None = None
    email: EmailStr | None = None
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None
    status: str | None = None


class UserPartialUpdateFull(UserPartialUpdate):
    password_hash: str | None = None


class UserInternal(APIModel):
    id: UUID
    username: str
    email: str
    password_hash: str
    permissions: set[str] | None = None
    avatar_attachment_id: UUID | None = None
    avatar_attachment: Attachment | None = None
    status: UserStatuses
    created_at: datetime


class UserSorts(enum.StrEnum):
    id = enum.auto()
    username = enum.auto()
    email = enum.auto()
    status = enum.auto()
    created_at = enum.auto()


class UpdatePasswordRequest(APIModel):
    email: str


class UpdatePasswordConfirm(APIModel):
    email: str | None = None
    code: str | None = None
    password: str | None = None


class UserProfilePartialUpdate(APIModel):
    username: str | None = None
    password: str | None = None


class PasswordResetCode(APIModel):
    user_id: UUID
    code: str


class PasswordResetCodePartialUpdate(APIModel):
    code: str | None = None


@dataclass
class UserListRequestSchema:
    pagination: pg.PaginationCallable[User] | None = None
    sorting: sr.SortingData[UserSorts] | None = None


@dataclass
class UserWhere:
    id: UUID | None = None
    username: str | None = None
    email: str | None = None


@dataclass
class PasswordResetCodeWhere:
    id: int | None = None
    user_id: UUID | None = None
    code: str | None = None
