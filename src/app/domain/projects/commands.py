from fastapi import HTTPException

from app.domain.common.exceptions import NotFoundError
from app.domain.common.models import EmailCode
from app.domain.projects.queries import ProjectRetrieveQuery
from app.domain.projects.repositories import ProjectRepository, LikeTheProjectRepository
from app.domain.projects.schemas import Project, ProjectCreate, LikeTheProject, Like
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.common.models import Project as ProjectModel

from app.domain.users.core.commands import UserCreateCommand
from app.domain.users.core.queries import UserRetrieveQuery
from app.domain.users.core.repositories import EmailRpository
from app.domain.users.core.schemas import UserCreate, UserDetails, UserCredentialsRegist, EmailForCode, VerificationCode
from a8t_tools.security.hashing import PasswordHashService
from app.domain.projects import schemas

from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.registration.hi import send_user_email_verification


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
        )

        await self.project_repository.create_project(create_project)


class LikeTheProjectCommand:
    def __init__(
            self,
            project_like_repository: LikeTheProjectRepository,
            project_retrieve_by_id_query: ProjectRetrieveQuery,
            current_user_query: CurrentUserQuery,
            project_repository: ProjectRepository
    ) -> None:
        self.project_like_repository = project_like_repository
        self.project_retrieve_by_id_query = project_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.project_repository = project_repository

    async def __call__(self, payload: Like) -> None:
        project_id = payload.project_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        # Получаем проект по его ID
        project = await self.project_retrieve_by_id_query(project_id)

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        # Увеличиваем счетчик лайков на объекте проекта
        new_likes_count = project.likes + 1

        # Сохраняем обновленное количество лайков в базе данных
        await self.project_repository.update_project_likes(project_id, new_likes_count)

        # Создаем запись о лайке (для истории или других нужд)
        create_like_the_project = schemas.LikeTheProject(
            project_id=project_id,
            user_id=user_id,
        )

        await self.project_like_repository.create_like_project(create_like_the_project)


class UnlikeTheProjectCommand:
    def __init__(
            self,
            project_like_repository: LikeTheProjectRepository,
            project_retrieve_by_id_query: ProjectRetrieveQuery,
            current_user_query: CurrentUserQuery,
            project_repository: ProjectRepository
    ) -> None:
        self.project_like_repository = project_like_repository
        self.project_retrieve_by_id_query = project_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.project_repository = project_repository

    async def __call__(self, payload: Like) -> None:
        project_id = payload.project_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        # Получаем проект по его ID
        project = await self.project_retrieve_by_id_query(project_id)

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        # Уменьшаем счетчик лайков на объекте проекта
        new_likes_count = project.likes - 1

        # Проверяем, что лайк действительно существует
        like_exists = await self.project_like_repository.check_like_exists(project_id, user_id)
        if not like_exists:
            raise HTTPException(status_code=404, detail="Like not found")

        # Удаляем лайк и обновляем количество лайков
        await self.project_repository.update_project_likes(project_id, new_likes_count)
        await self.project_like_repository.delete_like_project(project_id, user_id)


class ProjectPartialUpdateCommand:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, project_id: int, payload: schemas.ProjectPartialUpdate) -> schemas.ProjectDetailsFull:
        try:
            await self.project_repository.partial_update_project(project_id, payload)
            user = await self.project_repository.get_project_by_filter_or_none(schemas.ProjectWhere(id=project_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении проекта:", e)
            raise

        return schemas.ProjectDetailsFull.model_validate(user)
