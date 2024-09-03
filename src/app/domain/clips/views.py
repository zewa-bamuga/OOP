from contextlib import asynccontextmanager

from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile, Header
from fastapi.params import Form

from app.api import deps
from app.containers import Container
from app.domain.clips.commands import ClipCreateCommand, LikeTheClipCommand
from app.domain.clips.queries import ClipRetrieveQuery, ClipManagementListQuery
from app.domain.clips.schemas import ClipCreate
from app.domain.projects.schemas import Like
from app.domain.clips import schemas
from app.domain.storage.attachments import schemas as AttachmentSchema
from app.domain.storage.attachments.commands import NewsAttachmentCreateCommand

from a8t_tools.security.tokens import override_user_token
from a8t_tools.db import pagination, sorting

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post(
    "/create/info",
    response_model=None
)
@wiring.inject
async def create_clip_info(
        payload: ClipCreate,
        token: str = Header(...),
        command: ClipCreateCommand = Depends(wiring.Provide[Container.clip.create_command]),
):
    async with user_token(token):
        clip = await command(payload)
        return clip


@router.post(
    "/create/attachment",
    response_model=AttachmentSchema.Attachment
)
@wiring.inject
async def create_clip_attachment(
        attachment: UploadFile,
        clip_id: int = Form(...),
        token: str = Header(...),
        command: NewsAttachmentCreateCommand = Depends(wiring.Provide[Container.attachment.clip_create_command]),
) -> AttachmentSchema.Attachment:
    payload = Like(clip_id=clip_id)

    async with user_token(token):
        return await command(payload,
                             AttachmentSchema.AttachmentCreate(
                                 file=attachment.file,
                                 name=attachment.filename,
                             ),
                             )


@router.get(
    "/get",
    response_model=pagination.CountPaginationResults[schemas.ClipDetailsFull],
)
@wiring.inject
async def get_clip_list(
        query: ClipManagementListQuery = Depends(wiring.Provide[Container.clip.management_list_query]),
        pagination: pagination.PaginationCallable[schemas.ClipDetailsFull] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.ClipDetailsFull)),
        sorting: sorting.SortingData[schemas.ClipSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.ClipSorts,
                schemas.ClipSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.ClipDetailsFull]:
    return await query(schemas.ClipListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/get/by/id/{news_id}",
    response_model=None
)
@wiring.inject
async def get_clip_by_id(
        clip_id: int,
        query: ClipRetrieveQuery = Depends(wiring.Provide[Container.clip.clip_retrieve_by_id_query]),
):
    clip = await query(clip_id)
    return clip


# Если один пользователь сначала отправляет лайк на фото, а потом отправляет опять, то лайк убирается
@router.post(
    "/like",
    response_model=None
)
@wiring.inject
async def like_the_clip(
        payload: Like,
        token: str = Header(...),
        command: LikeTheClipCommand = Depends(wiring.Provide[Container.clip.like_the_clip_command]),
):
    async with user_token(token):
        clip = await command(payload)
        return clip
