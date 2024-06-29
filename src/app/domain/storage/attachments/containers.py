from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.containers import UserContainer


class AttachmentContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    file_storage = providers.Dependency(instance_of=FileStorage)

    bucket = providers.Dependency(instance_of=str)

    repository = providers.Factory(AttachmentRepository, transaction=transaction)

    list_query = providers.Factory(AttachmentListQuery, repository=repository)

    retrieve_query = providers.Factory(AttachmentRetrieveQuery, repository=repository)

    user_container = providers.Container(UserContainer)  # Добавляем зависимость от UserContainer

    create_command = providers.Factory(
        AttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
        current_user_query=user_container.profile_me_query,
        user_partial_update_command=user_container.partial_update_command,
    )
