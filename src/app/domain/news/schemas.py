import enum
from dataclasses import dataclass
from datetime import datetime
from typing import IO
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
