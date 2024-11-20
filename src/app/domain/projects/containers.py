from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction

from app.domain.projects.commands import ProjectCreateCommand, LikeTheProjectCommand, UnlikeTheProjectCommand, \
    ProjectPartialUpdateCommand, AddEmployeesCommand, ProjectDeleteCommand, ProjectAttachmentDeleteCommand, \
    ProjectStaffDeleteCommand
from app.domain.projects.queries import ProjectManagementListQuery, ProjectListQuery, ProjectRetrieveQuery, \
    ProjectStaffManagementListQuery, ProjectStaffListQuery, ProjectAttachmentManagementListQuery, \
    ProjectAttachmentListQuery
from app.domain.projects.repositories import ProjectRepository, LikeTheProjectRepository, ProjectStaffRepository, \
    ProjectAttachmentRepository
from app.domain.users.containers import UserContainer


class ProjectContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    project_repository = providers.Factory(ProjectRepository, transaction=transaction)
    project_like_repository = providers.Factory(LikeTheProjectRepository, transaction=transaction)
    project_staff_repository = providers.Factory(ProjectStaffRepository, transaction=transaction)
    project_attachment_repository = providers.Factory(ProjectAttachmentRepository, transaction=transaction)

    user_container = providers.Container(UserContainer)

    create_command = providers.Factory(
        ProjectCreateCommand,
        project_repository=project_repository,
    )

    delete_project = providers.Factory(
        ProjectDeleteCommand,
        project_repository=project_repository,
    )

    create_add_employees_command = providers.Factory(
        AddEmployeesCommand,
        project_staff_repository=project_staff_repository,
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

    delete_project_attachment_command = providers.Factory(
        ProjectAttachmentDeleteCommand,
        project_attachment_repository=project_attachment_repository,
    )

    delete_project_staff_command = providers.Factory(
        ProjectStaffDeleteCommand,
        project_staff_repository=project_staff_repository,
    )

    project_list_query = providers.Factory(
        ProjectListQuery,
        project_repository=project_repository,
    )

    project_attachment_list_query = providers.Factory(
        ProjectAttachmentListQuery,
        project_attachment_repository=project_attachment_repository,
    )

    project_staff_list_query = providers.Factory(
        ProjectStaffListQuery,
        project_staff_repository=project_staff_repository,
    )

    management_list_query = providers.Factory(
        ProjectManagementListQuery,
        query=project_list_query,
    )

    project_attachment_management_list_query = providers.Factory(
        ProjectAttachmentManagementListQuery,
        query=project_attachment_list_query,
    )

    staff_management_list_query = providers.Factory(
        ProjectStaffManagementListQuery,
        query=project_staff_list_query,
    )
