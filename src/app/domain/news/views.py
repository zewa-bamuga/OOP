from contextlib import asynccontextmanager

from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile, Header
from fastapi.params import Form

from app.api import deps
from app.containers import Container
from app.domain.news.commands import NewsCreateCommand, LikeTheNewsCommand, UnlikeTheNewsCommand
from app.domain.news.queries import NewsRetrieveQuery, NewsManagementListQuery
from app.domain.news.schemas import NewsCreate
from app.domain.projects.schemas import Like
from app.domain.news import schemas
from app.domain.storage.attachments import schemas as AttachmentSchema
from app.domain.storage.attachments.commands import NewsAttachmentCreateCommand

from a8t_tools.db import pagination, sorting
from a8t_tools.security.tokens import override_user_token

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post(
    "/create",
    response_model=None
)
@wiring.inject
async def create_news(
        payload: NewsCreate,
        token: str = Header(...),
        command: NewsCreateCommand = Depends(wiring.Provide[Container.news.create_command]),
):
    async with user_token(token):
        news = await command(payload)
        return news


@router.post(
    "/create/attachment",
    response_model=AttachmentSchema.Attachment
)
@wiring.inject
async def create_news_attachment(
        attachment: UploadFile,
        news_id: int = Form(...),
        token: str = Header(...),
        command: NewsAttachmentCreateCommand = Depends(wiring.Provide[Container.attachment.news_create_command]),
) -> AttachmentSchema.Attachment:
    payload = Like(news_id=news_id)

    async with user_token(token):
        return await command(payload,
                             AttachmentSchema.AttachmentCreate(
                                 file=attachment.file,
                                 name=attachment.filename,
                             ),
                             )


@router.get(
    "/get",
    response_model=pagination.CountPaginationResults[schemas.NewsDetailsFull],
)
@wiring.inject
async def get_news_list(
        query: NewsManagementListQuery = Depends(wiring.Provide[Container.news.management_list_query]),
        pagination: pagination.PaginationCallable[schemas.NewsDetailsFull] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.NewsDetailsFull)),
        sorting: sorting.SortingData[schemas.NewsSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.NewsSorts,
                schemas.NewsSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.NewsDetailsFull]:
    return await query(schemas.NewsListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/get/by/id/{news_id}",
    response_model=None
)
@wiring.inject
async def get_news_by_id(
        news_id: int,
        query: NewsRetrieveQuery = Depends(wiring.Provide[Container.news.news_retrieve_by_id_query]),
):
    news = await query(news_id)
    return news


@router.post(
    "/like",
    response_model=None
)
@wiring.inject
async def like_the_news(
        payload: Like,
        token: str = Header(...),
        command: LikeTheNewsCommand = Depends(wiring.Provide[Container.news.like_the_news_command]),
):
    async with user_token(token):
        news = await command(payload)
        return news


@router.delete(
    "/unlike",
    response_model=None
)
@wiring.inject
async def unlike_the_news(
        payload: Like,
        token: str = Header(...),
        command: UnlikeTheNewsCommand = Depends(wiring.Provide[Container.news.unlike_the_news_command]),
):
    async with user_token(token):
        await command(payload)
        return {"status": "success"}
