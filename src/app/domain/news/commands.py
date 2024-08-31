from fastapi import HTTPException

from app.domain.common.exceptions import NotFoundError
from app.domain.common.models import EmailCode
from app.domain.news.repositories import NewsRepository
from app.domain.news.schemas import NewsCreate
from app.domain.projects.queries import ProjectRetrieveQuery
from app.domain.projects.repositories import ProjectRepository, LikeTheProjectRepository, AddEmployeesRepository
from app.domain.projects.schemas import Project, ProjectCreate, LikeTheProject, Like, AddEmployees
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.common.models import Project as ProjectModel

from app.domain.users.core.commands import UserCreateCommand
from app.domain.users.core.queries import UserRetrieveQuery
from app.domain.users.core.repositories import EmailRpository
from app.domain.users.core.schemas import UserCreate, UserDetails, UserCredentialsRegist, EmailForCode, VerificationCode
from a8t_tools.security.hashing import PasswordHashService
from app.domain.news import schemas

from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.registration.hi import send_user_email_verification


class NewsCreateCommand:
    def __init__(
            self,
            news_repository: NewsRepository,
    ) -> None:
        self.news_repository = news_repository

    async def __call__(self, payload: NewsCreate) -> None:
        create_news = schemas.NewsCreate(
            name=payload.name,
            date=payload.date,
            description=payload.description,
        )

        await self.news_repository.create_news(create_news)
