from uuid import UUID

from app.domain.projects.repositories import ProjectRepository, ProjectStaffRepository
from app.domain.projects.schemas import ProjectListRequestSchema, ProjectStaffListRequestSchema
from app.domain.projects import schemas

from a8t_tools.db.pagination import Paginated


class ProjectListQuery:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, payload: schemas.ProjectListRequestSchema) -> Paginated[schemas.Project]:
        return await self.project_repository.get_project(payload.pagination, payload.sorting)


class ProjectStaffListQuery:
    def __init__(self, project_staff_repository: ProjectStaffRepository):
        self.project_staff_repository = project_staff_repository

    async def __call__(self, payload: schemas.ProjectStaffListRequestSchema) -> Paginated[
        schemas.ProjectStaffDetailsShort]:
        return await self.project_staff_repository.get_project_staff(payload.pagination, payload.sorting)


class ProjectManagementListQuery:
    def __init__(self, query: ProjectListQuery) -> None:
        self.query = query

    async def __call__(self, payload: ProjectListRequestSchema) -> Paginated[schemas.Project]:
        return await self.query(payload)


class ProjectRetrieveQuery:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, project_id: UUID) -> schemas.ProjectDetailsFull:
        project_result = await self.project_repository.get_project_by_filter_or_none(
            schemas.ProjectWhere(id=project_id))
        return schemas.ProjectDetailsFull.model_validate(project_result)


class ProjectStaffManagementListQuery:
    def __init__(self, query: ProjectStaffListQuery) -> None:
        self.query = query

    async def __call__(self, payload: ProjectStaffListRequestSchema) -> Paginated[schemas.ProjectStaffDetailsShort]:
        return await self.query(payload)
