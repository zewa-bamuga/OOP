from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

from app.domain.news.commands import NewsCreateCommand
from app.domain.news.repositories import NewsRepository
from app.domain.projects.commands import ProjectCreateCommand, LikeTheProjectCommand, UnlikeTheProjectCommand, \
    ProjectPartialUpdateCommand, AddEmployeesCommand
from app.domain.projects.queries import ProjectManagementListQuery, ProjectListQuery, ProjectRetrieveQuery
from app.domain.projects.repositories import ProjectRepository, LikeTheProjectRepository, AddEmployeesRepository
from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.users.containers import UserContainer


class NewsContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    news_repository = providers.Factory(NewsRepository, transaction=transaction)

    user_container = providers.Container(UserContainer)

    create_command = providers.Factory(
        NewsCreateCommand,
        news_repository=news_repository,
    )