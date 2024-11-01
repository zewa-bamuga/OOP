from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile, Header
from fastapi.params import Form

from app.api import deps
from app.containers import Container
from app.domain.projects.queries import ProjectManagementListQuery, ProjectRetrieveQuery, \
    ProjectStaffManagementListQuery
from app.domain.projects.schemas import ProjectCreate, Like, AddEmployees
from app.domain.projects.commands import ProjectCreateCommand, LikeTheProjectCommand, UnlikeTheProjectCommand, \
    AddEmployeesCommand
from app.domain.projects import schemas
from app.domain.users.core import schemas as schemas_staff
from app.domain.storage.attachments import schemas as AttachmentSchema
from app.domain.storage.attachments.commands import ProjectAttachmentCreateCommand

from a8t_tools.db import pagination, sorting

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
async def create_projects(
        payload: ProjectCreate,
        token: str = Header(...),
        command: ProjectCreateCommand = Depends(wiring.Provide[Container.project.create_command]),
):
    async with user_token(token):
        project = await command(payload)
        return project


@router.post(
    "/add/employees",
    response_model=None
)
@wiring.inject
async def add_employees(
        payload: AddEmployees,
        token: str = Header(...),
        command: AddEmployeesCommand = Depends(wiring.Provide[Container.project.create_add_employees_command]),
):
    async with user_token(token):
        project = await command(payload)
        return project


@router.post(
    "/create/attachment",
    response_model=AttachmentSchema.Attachment
)
@wiring.inject
async def create_project_attachment(
        attachment: UploadFile,
        project_id: int = Form(...),
        token: str = Header(...),
        command: ProjectAttachmentCreateCommand = Depends(wiring.Provide[Container.attachment.project_create_command]),
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
    "/get",
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
    "/project/by/id/{project_id}",
    response_model=None
)
@wiring.inject
async def get_project_by_id(
        project_id: UUID,
        query: ProjectRetrieveQuery = Depends(wiring.Provide[Container.project.project_retrieve_by_id_query]),
):
    project = await query(project_id)
    return project


@router.get(
    "/get/staff",
    response_model=pagination.CountPaginationResults[schemas.ProjectStaffDetailsShort],
)
@wiring.inject
async def get_project_staff_list(
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
    return await query(schemas.ProjectStaffListRequestSchema(pagination=pagination, sorting=sorting))


@router.post(
    "/like",
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
    "/unlike",
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
