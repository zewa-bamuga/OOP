from fastapi import HTTPException

from app.domain.clips.queries import ClipRetrieveQuery
from app.domain.clips.repositories import ClipRepository, LikeClipRepository
from app.domain.clips.schemas import ClipCreate
from app.domain.common.exceptions import NotFoundError
from app.domain.projects.schemas import Like
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.clips import schemas


class ClipCreateCommand:
    def __init__(
            self,
            clip_repository: ClipRepository,
    ) -> None:
        self.clip_repository = clip_repository

    async def __call__(self, payload: ClipCreate) -> None:
        create_clip = schemas.ClipCreate(
            name=payload.name,
            date=payload.date,
            description=payload.description,
        )

        await self.clip_repository.create_clip(create_clip)


class ClipPartialUpdateCommand:
    def __init__(self, clip_repository: ClipRepository):
        self.clip_repository = clip_repository

    async def __call__(self, clip_id: int, payload: schemas.ClipPartialUpdate) -> schemas.ClipDetailsFull:
        try:
            await self.clip_repository.partial_update_clip(clip_id, payload)
            user = await self.clip_repository.get_clip_by_filter_or_none(schemas.ClipWhere(id=clip_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении новости:", e)
            raise

        return schemas.ClipDetailsFull.model_validate(user)


class ClipDeleteCommand:
    def __init__(
            self,
            clip_repository: ClipRepository,
            clip_like_repository: LikeClipRepository,
    ) -> None:
        self.clip_repository = clip_repository
        self.clip_like_repository = clip_like_repository

    async def __call__(self, clip_id: int) -> None:
        # await self.clip_like_repository.delete_like_clip(clip_id)
        return await self.clip_repository.delete_clip(clip_id)


class LikeTheClipCommand:
    def __init__(
            self,
            clip_like_repository: LikeClipRepository,
            clip_retrieve_by_id_query: ClipRetrieveQuery,
            current_user_query: CurrentUserQuery,
            clip_repository: ClipRepository
    ) -> None:
        self.clip_like_repository = clip_like_repository
        self.clip_retrieve_by_id_query = clip_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.clip_repository = clip_repository

    async def __call__(self, payload: Like) -> None:
        clip_id = payload.clip_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        clip = await self.clip_retrieve_by_id_query(clip_id)

        if clip is None:
            raise HTTPException(status_code=404, detail="Clip not found")

        clip_likes_count = clip.likes + 1

        create_like_the_clip = schemas.LikeTheClip(
            clip_id=clip_id,
            user_id=user_id,
        )
        await self.clip_like_repository.create_like_clip(create_like_the_clip)

        await self.clip_repository.update_clip_likes(clip_id, clip_likes_count)


class UnlikeTheClipCommand:
    def __init__(
            self,
            clip_like_repository: LikeClipRepository,
            clip_retrieve_by_id_query: ClipRetrieveQuery,
            current_user_query: CurrentUserQuery,
            clip_repository: ClipRepository
    ) -> None:
        self.clip_like_repository = clip_like_repository
        self.clip_retrieve_by_id_query = clip_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.clip_repository = clip_repository

    async def __call__(self, payload: Like) -> None:
        clip_id = payload.clip_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        clip = await self.clip_retrieve_by_id_query(clip_id)

        if clip is None:
            raise HTTPException(status_code=404, detail="Clip not found")

        new_likes_count = clip.likes - 1

        like_exists = await self.clip_like_repository.check_like_exists(clip_id, user_id)
        if not like_exists:
            raise HTTPException(status_code=404, detail="Like not found")

        await self.clip_repository.update_clip_likes(clip_id, new_likes_count)
        await self.clip_like_repository.delete_like_clip(clip_id, user_id)
