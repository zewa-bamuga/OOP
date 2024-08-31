from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

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


class ProjectContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    project_repository = providers.Factory(ProjectRepository, transaction=transaction)
    project_like_repository = providers.Factory(LikeTheProjectRepository, transaction=transaction)
    add_employees_repository = providers.Factory(AddEmployeesRepository, transaction=transaction)

    user_container = providers.Container(UserContainer)

    create_command = providers.Factory(
        ProjectCreateCommand,
        project_repository=project_repository,
    )

    create_add_employees_command = providers.Factory(
        AddEmployeesCommand,
        add_employees_project_repository=add_employees_repository,
    )

    project_retrieve_by_id_query = providers.Factory(
        ProjectRetrieveQuery,
        project_repository=project_repository,
    )

    project_partial_update_command = providers.Factory(
        ProjectPartialUpdateCommand,
        project_repository=project_repository,
    )

    current_project_query = providers.Factory(
        ProjectRetrieveQuery,
        project_repository=project_repository
    )

    like_the_project_command = providers.Factory(
        LikeTheProjectCommand,
        project_like_repository=project_like_repository,
        project_retrieve_by_id_query=project_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        project_repository=project_repository,
    )

    unlike_the_project_command = providers.Factory(
        UnlikeTheProjectCommand,
        project_like_repository=project_like_repository,
        project_retrieve_by_id_query=project_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        project_repository=project_repository,
    )

    project_list_query = providers.Factory(
        ProjectListQuery,
        project_repository=project_repository,
    )

    management_list_query = providers.Factory(
        ProjectManagementListQuery,
        query=project_list_query,
    )
