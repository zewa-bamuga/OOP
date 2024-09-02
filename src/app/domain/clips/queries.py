from app.domain.clips.repositories import ClipRepository
from app.domain.news.repositories import NewsRepository
from app.domain.news.schemas import NewsListRequestSchema
from app.domain.clips import schemas

from a8t_tools.db.pagination import Paginated


class ClipRetrieveQuery:
    def __init__(self, clip_repository: ClipRepository):
        self.clip_repository = clip_repository

    async def __call__(self, clip_id: int) -> schemas.ClipDetailsFull:
        clip_result = await self.clip_repository.get_clip_by_filter_or_none(
            schemas.ClipWhere(id=clip_id))
        return schemas.ClipDetailsFull.model_validate(clip_result)
