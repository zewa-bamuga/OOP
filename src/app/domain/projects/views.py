from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile, Header
from fastapi.params import Form
from starlette import status

from app.api import deps
from app.containers import Container
from app.domain.clips.commands import ClipDeleteCommand
from app.domain.clips.schemas import ClipDelete
from app.domain.projects.queries import ProjectManagementListQuery, ProjectRetrieveQuery, \
    ProjectStaffManagementListQuery
from app.domain.projects.schemas import ProjectCreate, Like, AddEmployees, ProjectDelete
from app.domain.projects.commands import ProjectCreateCommand, LikeTheProjectCommand, UnlikeTheProjectCommand, \
    AddEmployeesCommand, ProjectDeleteCommand, ProjectAttachmentDeleteCommand, ProjectStaffDeleteCommand, \
    ProjectPartialUpdateCommand
from app.domain.projects import schemas
from app.domain.storage.attachments import schemas as AttachmentSchema
from app.domain.storage.attachments.commands import ProjectAttachmentCreateCommand, ProjectAvatarCreateCommand

from a8t_tools.db import pagination, sorting

from app.domain.users.profile.commands import UserProfilePartialUpdateCommand

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
async def create_project(
        payload: ProjectCreate,
        token: str = Header(...),
        command: ProjectCreateCommand = Depends(wiring.Provide[Container.project.create_command]),
):
    async with user_token(token):
        project = await command(payload)
        return project


@router.get(
    "/get/list",
    response_model=pagination.CountPaginationResults[schemas.ProjectDetailsFull],
)
@wiring.inject
async def get_projects_list(
        query: ProjectManagementListQuery = Depends(wiring.Provide[Container.project.management_list_query]),
        pagination: pagination.PaginationCallable[schemas.ProjectDetailsFull] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.ProjectDetailsFull)),
        sorting: sorting.SortingData[schemas.ProjectSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.ProjectSorts,
                schemas.ProjectSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.ProjectDetailsFull]:
    return await query(schemas.ProjectListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/get/{project_id}",
    response_model=None
)
@wiring.inject
async def get_project_by_id(
        project_id: UUID,
        query: ProjectRetrieveQuery = Depends(wiring.Provide[Container.project.project_retrieve_by_id_query]),
):
    project = await query(project_id)
    return project


@router.patch(
    "/avatar/update",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def update_avatar(
        payload: schemas.ProjectPartialUpdate,
        command: ProjectPartialUpdateCommand = Depends(
            wiring.Provide[Container.project.project_partial_update_command]),
) -> None:
    await command(payload)


@router.delete(
    "/delete",
    response_model=None
)
@wiring.inject
async def delete_project(
        payload: ProjectDelete,
        token: str = Header(...),
        command: ProjectDeleteCommand = Depends(wiring.Provide[Container.project.delete_project]),
):
    async with user_token(token):
        return await command(payload)


@router.post(
    "/add/staff",
    response_model=None
)
@wiring.inject
async def add_staff(
        payload: AddEmployees,
        token: str = Header(...),
        command: AddEmployeesCommand = Depends(wiring.Provide[Container.project.create_add_employees_command]),
):
    async with user_token(token):
        project = await command(payload)
        return project


@router.get(
    "/get/staff/list",
    response_model=pagination.CountPaginationResults[schemas.ProjectStaffDetailsShort],
)
@wiring.inject
async def get_project_staff_list(
        project_id: UUID,
        query: ProjectStaffManagementListQuery = Depends(wiring.Provide[Container.project.staff_management_list_query]),
        pagination: pagination.PaginationCallable[schemas.ProjectStaffDetailsShort] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.ProjectStaffDetailsShort)),
        sorting: sorting.SortingData[schemas.ProjectStaffSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.ProjectStaffSorts,
                schemas.ProjectStaffSorts.project_id,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.ProjectStaffDetailsShort]:
    return await query(
        schemas.ProjectStaffListRequestSchema(project_id=project_id, pagination=pagination, sorting=sorting))


@router.delete(
    "/delete/staff",
    response_model=None
)
@wiring.inject
async def delete_project_staff(
        payload: AddEmployees,
        token: str = Header(...),
        command: ProjectStaffDeleteCommand = Depends(wiring.Provide[Container.project.delete_project_staff_command]),
):
    async with user_token(token):
        await command(payload)
        return {"status": "success"}


@router.post(
    "/create/avatar",
    response_model=AttachmentSchema.Attachment
)
@wiring.inject
async def create_project_avatar(
        attachment: UploadFile,
        project_id: UUID = Form(...),
        token: str = Header(...),
        command: ProjectAvatarCreateCommand = Depends(wiring.Provide[Container.attachment.project_create_command]),
) -> AttachmentSchema.Attachment:
    payload = Like(project_id=project_id)

    async with user_token(token):
        return await command(payload,
                             AttachmentSchema.AttachmentCreate(
                                 file=attachment.file,
                                 name=attachment.filename,
                             ),
                             )


# @router.patch(
#    "/update/avatar",
#    response_model=None
# )
# @wiring.inject
# async def update_project_avatar(
#        attachment: UploadFile,
#       payload: schemas.ProjectAttachment,
#        token: str = Header(...),
#        command: ProjectAvatarUpdateCommand = Depends(
#            wiring.Provide[Container.project.delete_project_attachment_command]),
# ) -> AttachmentSchema.Attachment:
#    async with user_token(token):
#        return await command(payload,
#                             AttachmentSchema.AttachmentCreate(
#                                 file=attachment.file,
#                                 name=attachment.filename,
#                             ),
#                             )


@router.post(
    "/create/attachment",
    response_model=AttachmentSchema.Attachment
)
@wiring.inject
async def create_project_attachment(
        attachment: UploadFile,
        project_id: UUID = Form(...),
        token: str = Header(...),
        command: ProjectAttachmentCreateCommand = Depends(
            wiring.Provide[Container.attachment.project_create_attachment_command]),
) -> AttachmentSchema.Attachment:
    payload = Like(project_id=project_id)

    async with user_token(token):
        return await command(payload,
                             AttachmentSchema.AttachmentCreate(
                                 file=attachment.file,
                                 name=attachment.filename,
                             ),
                             )


@router.get(
    "/get/attachment/list",
    response_model=pagination.CountPaginationResults[schemas.ProjectAttachmentDetailsShort],
)
@wiring.inject
async def get_project_attachment_list(
        project_id: UUID,
        query: ProjectStaffManagementListQuery = Depends(
            wiring.Provide[Container.project.project_attachment_management_list_query]),
        pagination: pagination.PaginationCallable[schemas.ProjectAttachmentDetailsShort] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.ProjectAttachmentDetailsShort)),
        sorting: sorting.SortingData[schemas.ProjectAttachmentSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.ProjectAttachmentSorts,
                schemas.ProjectAttachmentSorts.project_id,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.ProjectAttachmentDetailsShort]:
    return await query(
        schemas.ProjectAttachmentListRequestSchema(project_id=project_id, pagination=pagination, sorting=sorting))


@router.delete(
    "/delete/attachment",
    response_model=None
)
@wiring.inject
async def delete_project_attachment(
        payload: schemas.ProjectAttachment,
        token: str = Header(...),
        command: ProjectAttachmentDeleteCommand = Depends(
            wiring.Provide[Container.project.delete_project_attachment_command]),
):
    async with user_token(token):
        await command(payload)
        return {"status": "success"}


@router.post(
    "/create/like",
    response_model=None
)
@wiring.inject
async def like_the_project(
        payload: Like,
        token: str = Header(...),
        command: LikeTheProjectCommand = Depends(wiring.Provide[Container.project.like_the_project_command]),
):
    async with user_token(token):
        project = await command(payload)
        return project


@router.delete(
    "/delete/like",
    response_model=None
)
@wiring.inject
async def unlike_the_project(
        payload: Like,
        token: str = Header(...),
        command: UnlikeTheProjectCommand = Depends(wiring.Provide[Container.project.unlike_the_project_command]),
):
    async with user_token(token):
        await command(payload)
        return {"status": "success"}
