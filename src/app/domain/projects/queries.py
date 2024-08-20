from uuid import UUID

from app.domain.projects.repositories import ProjectRepository
from app.domain.projects.schemas import ProjectListRequestSchema
from app.domain.users.core.queries import UserListQuery, UserRetrieveQuery, EmailRetrieveQuery
from app.domain.users.core.schemas import User, UserDetailsFull, UserListRequestSchema, StaffListRequestSchema, Staff
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService
from a8t_tools.db.pagination import Paginated
from app.domain.projects import schemas


class ProjectListQuery:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, payload: schemas.ProjectListRequestSchema) -> Paginated[schemas.Project]:
        return await self.project_repository.get_project(payload.pagination, payload.sorting)


class ProjectManagementListQuery:
    def __init__(self, query: ProjectListQuery) -> None:
        self.query = query

    async def __call__(self, payload: ProjectListRequestSchema) -> Paginated[schemas.Project]:
        return await self.query(payload)


class ProjectRetrieveQuery:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, project_id: int) -> schemas.Project:
        project_result = await self.project_repository.get_project_by_filter_or_none(schemas.ProjectWhere(id=project_id))
        return schemas.Project.model_validate(project_result)
