from a8t_tools.db.pagination import Paginated

from app.domain.clips import schemas
from app.domain.clips.repositories import ClipRepository
from app.domain.clips.schemas import ClipListRequestSchema


class ClipRetrieveQuery:
    def __init__(self, clip_repository: ClipRepository):
        self.clip_repository = clip_repository

    async def __call__(self, clip_id: int) -> schemas.ClipDetailsFull:
        clip_result = await self.clip_repository.get_clip_by_filter_or_none(
            schemas.ClipWhere(id=clip_id)
        )
        return schemas.ClipDetailsFull.model_validate(clip_result)


class ClipListQuery:
    def __init__(self, clip_repository: ClipRepository):
        self.clip_repository = clip_repository

    async def __call__(
        self, payload: schemas.ClipListRequestSchema
    ) -> Paginated[schemas.Clip]:
        return await self.clip_repository.get_clip(payload.pagination, payload.sorting)


class ClipManagementListQuery:
    def __init__(self, query: ClipListQuery) -> None:
        self.query = query

    async def __call__(self, payload: ClipListRequestSchema) -> Paginated[schemas.Clip]:
        return await self.query(payload)
