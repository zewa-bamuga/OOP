from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

from app.domain.clips.containers import ClipContainer
from app.domain.news.containers import NewsContainer
from app.domain.projects.containers import ProjectContainer
from app.domain.projects.repositories import ProjectAttachmentRepository
from app.domain.storage.attachments.commands import AttachmentCreateCommand, ProjectAttachmentCreateCommand, \
    NewsAttachmentCreateCommand, ClipAttachmentCreateCommand, ProjectAvatarCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.users.containers import UserContainer
from app.domain.users.staff.command import StaffAvatarCreateCommand


class AttachmentContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    file_storage = providers.Dependency(instance_of=FileStorage)

    bucket = providers.Dependency(instance_of=str)

    repository = providers.Factory(AttachmentRepository, transaction=transaction)

    project_attachment_repository = providers.Factory(ProjectAttachmentRepository, transaction=transaction)

    list_query = providers.Factory(AttachmentListQuery, repository=repository)

    retrieve_query = providers.Factory(AttachmentRetrieveQuery, repository=repository)

    user_container = providers.Container(UserContainer)

    project_container = providers.Container(ProjectContainer)

    news_container = providers.Container(NewsContainer)

    clip_container = providers.Container(ClipContainer)

    create_command = providers.Factory(
        AttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_user_query=user_container.profile_me_query,
        user_partial_update_command=user_container.partial_update_command,
    )

    project_create_command = providers.Factory(
        ProjectAvatarCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_project_query=project_container.current_project_query,
        project_partial_update_command=project_container.project_partial_update_command,
    )

    staff_create_command = providers.Factory(
        StaffAvatarCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        staff_retrieve_by_id_query=user_container.staff_retrieve_by_id_query,
        staff_partial_update_command=user_container.staff_partial_update_command,
    )

    project_create_attachment_command = providers.Factory(
        ProjectAttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_project_query=project_container.current_project_query,
        project_partial_update_command=project_container.project_partial_update_command,
        project_attachment_repository=project_attachment_repository
    )

    news_create_command = providers.Factory(
        NewsAttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_news_query=news_container.current_news_query,
        news_partial_update_command=news_container.news_partial_update_command,
    )

    clip_create_command = providers.Factory(
        ClipAttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_clip_query=clip_container.current_clip_query,
        clip_partial_update_command=clip_container.clip_partial_update_command,
    )
