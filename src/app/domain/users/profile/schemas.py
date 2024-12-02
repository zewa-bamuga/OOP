from uuid import UUID

from app.domain.common.schemas import APIModel


class UserProfilePartialUpdate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    description: str | None = None
    avatar_attachment_id: UUID | None = None
