from uuid import UUID

from app.domain.common.schemas import APIModel


class UserProfilePartialUpdate(APIModel):
    description: str | None = None
