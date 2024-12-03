from fastapi import HTTPException

from app.domain.common.exceptions import NotFoundError
from app.domain.projects import schemas
from app.domain.projects.queries import ProjectRetrieveQuery
from app.domain.projects.repositories import (
    LikeTheProjectRepository,
    ProjectAttachmentRepository,
    ProjectRepository,
    ProjectStaffRepository,
)
from app.domain.projects.schemas import (
    AddEmployees,
    Like,
    ProjectAttachment,
    ProjectCreate,
    ProjectDelete,
)
from app.domain.users.auth.queries import CurrentUserQuery


class ProjectCreateCommand:
    def __init__(
        self,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_repository = project_repository

    async def __call__(self, payload: ProjectCreate) -> None:
        create_project = schemas.ProjectCreate(
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            description=payload.description,
            participants=payload.participants,
            lessons=payload.lessons,
        )

        await self.project_repository.create_project(create_project)


class ProjectDeleteCommand:
    def __init__(
        self,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_repository = project_repository

    async def __call__(self, payload: ProjectDelete) -> None:
        return await self.project_repository.delete_project(payload)


class AddEmployeesCommand:
    def __init__(
        self,
        project_staff_repository: ProjectStaffRepository,
    ) -> None:
        self.project_staff_repository = project_staff_repository

    async def __call__(self, payload: AddEmployees) -> None:
        project_id = payload.project_id
        staff_id = payload.staff_id

        create_like_the_project = schemas.AddEmployees(
            project_id=project_id,
            staff_id=staff_id,
        )

        await self.project_staff_repository.create_add_staff_project(
            create_like_the_project
        )


class LikeTheProjectCommand:
    def __init__(
        self,
        project_like_repository: LikeTheProjectRepository,
        project_retrieve_by_id_query: ProjectRetrieveQuery,
        current_user_query: CurrentUserQuery,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_like_repository = project_like_repository
        self.project_retrieve_by_id_query = project_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.project_repository = project_repository

    async def __call__(self, payload: Like) -> None:
        project_id = payload.project_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        project = await self.project_retrieve_by_id_query(project_id)

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        like_exists = await self.project_like_repository.check_like_exists(
            project_id, user_id
        )

        if like_exists:
            new_likes_count = project.likes - 1
            await self.project_like_repository.delete_like_project(project_id, user_id)
        else:
            new_likes_count = project.likes + 1
            create_like_the_project = schemas.LikeTheProject(
                project_id=project_id,
                user_id=user_id,
            )
            await self.project_like_repository.create_like_project(
                create_like_the_project
            )

        await self.project_repository.update_project_likes(project_id, new_likes_count)


class UnlikeTheProjectCommand:
    def __init__(
        self,
        project_like_repository: LikeTheProjectRepository,
        project_retrieve_by_id_query: ProjectRetrieveQuery,
        current_user_query: CurrentUserQuery,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_like_repository = project_like_repository
        self.project_retrieve_by_id_query = project_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.project_repository = project_repository

    async def __call__(self, payload: Like) -> None:
        project_id = payload.project_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        project = await self.project_retrieve_by_id_query(project_id)

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        new_likes_count = project.likes - 1

        like_exists = await self.project_like_repository.check_like_exists(
            project_id, user_id
        )
        if not like_exists:
            raise HTTPException(status_code=404, detail="Like not found")

        await self.project_repository.update_project_likes(project_id, new_likes_count)
        await self.project_like_repository.delete_like_project(project_id, user_id)


class ProjectPartialUpdateCommand:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(
        self, payload: schemas.ProjectPartialUpdate
    ) -> schemas.ProjectDetailsFull:
        try:
            await self.project_repository.partial_update_project(payload)
            user = await self.project_repository.get_project_by_filter_or_none(
                schemas.ProjectWhere(id=payload.id)
            )

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении проекта:", e)
            raise

        return schemas.ProjectDetailsFull.model_validate(user)


class ProjectAttachmentDeleteCommand:
    def __init__(
        self,
        project_attachment_repository: ProjectAttachmentRepository,
    ) -> None:
        self.project_attachment_repository = project_attachment_repository

    async def __call__(self, payload: ProjectAttachment) -> None:
        return await self.project_attachment_repository.delete_project_attachment(
            payload
        )


class ProjectStaffDeleteCommand:
    def __init__(
        self,
        project_staff_repository: ProjectStaffRepository,
    ) -> None:
        self.project_staff_repository = project_staff_repository

    async def __call__(self, payload: ProjectAttachment) -> None:
        return await self.project_staff_repository.delete_staff_project(payload)
