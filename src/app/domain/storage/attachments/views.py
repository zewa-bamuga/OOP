from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.db import pagination, sorting
from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, Header, UploadFile

from app.api import deps
from app.containers import Container
from app.domain.storage.attachments import schemas
from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post("/create", response_model=schemas.Attachment)
@wiring.inject
async def create_attachment(
    attachment: UploadFile,
    token: str = Header(...),
    command: AttachmentCreateCommand = Depends(
        wiring.Provide[Container.attachment.create_command]
    ),
) -> schemas.Attachment:
    async with user_token(token):
        return await command(
            schemas.AttachmentCreate(
                file=attachment.file,
                name=attachment.filename,
            ),
        )


@router.get(
    "/get",
    response_model=pagination.CountPaginationResults[schemas.Attachment],
)
@wiring.inject
async def get_attachments_list(
    query: AttachmentListQuery = Depends(
        wiring.Provide[Container.attachment.list_query]
    ),
    pagination: pagination.PaginationCallable[schemas.Attachment] = Depends(
        deps.get_skip_limit_pagination_dep(schemas.Attachment)
    ),
    sorting: sorting.SortingData[schemas.AttachmentSorts] = Depends(
        deps.get_sort_order_sorting_dep(schemas.AttachmentSorts)
    ),
) -> pagination.Paginated[schemas.Attachment]:
    return await query(
        schemas.AttachmentListRequestSchema(pagination=pagination, sorting=sorting)
    )


@router.get(
    "/{attachment_id}",
    response_model=schemas.Attachment,
)
@wiring.inject
async def get_attachment_details(
    attachment_id: UUID,
    query: AttachmentRetrieveQuery = Depends(
        wiring.Provide[Container.attachment.retrieve_query]
    ),
) -> schemas.Attachment:
    return await query(attachment_id)
