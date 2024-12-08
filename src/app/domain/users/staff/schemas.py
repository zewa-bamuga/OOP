from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.schemas.pydantic import APIModel
from pydantic import EmailStr

from app.domain.storage.attachments.schemas import Attachment


class Staff(APIModel):
    id: UUID
    firstname: str | None = None
    lastname: str | None = None
    qualification: str | None = None
    post: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    link_to_vk: str | None = None
    avatar_attachment_id: UUID | None = None
    created_at: datetime


class StaffDetails(Staff):
    avatar_attachment: Attachment | None = None


class StaffInternal(APIModel):
    id: UUID
    firstname: str
    lastname: str
    qualification: str | None = None
    post: str | None = None
    email: EmailStr
    description: str | None = None
    link_to_vk: str | None = None
    avatar_attachment_id: UUID | None = None
    avatar_attachment: Attachment | None = None
    created_at: datetime


class StaffCreate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    qualification: str | None = None
    post: str | None = None
    description: str | None = None
    link_to_vk: str | None = None


class StaffDelete(APIModel):
    id: UUID


class StaffPartialUpdate(APIModel):
    avatar_attachment_id: UUID | None = None


class StaffDetailsFull(Staff):
    avatar_attachment: Attachment | None = None


@dataclass
class StaffWhere:
    id: UUID | None = None
    firstname: str | None = None
    email: str | None = None
