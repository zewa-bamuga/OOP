from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction

from app.domain.clips.commands import ClipCreateCommand, ClipPartialUpdateCommand, LikeTheClipCommand
from app.domain.clips.queries import ClipRetrieveQuery, ClipManagementListQuery, ClipListQuery
from app.domain.clips.repositories import ClipRepository, LikeClipRepository
from app.domain.users.containers import UserContainer


class ClipContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    clip_repository = providers.Factory(ClipRepository, transaction=transaction)

    clip_like_repository = providers.Factory(LikeClipRepository, transaction=transaction)

    user_container = providers.Container(UserContainer)

    create_command = providers.Factory(
        ClipCreateCommand,
        clip_repository=clip_repository,
    )

    current_clip_query = providers.Factory(
        ClipRetrieveQuery,
        clip_repository=clip_repository
    )

    clip_partial_update_command = providers.Factory(
        ClipPartialUpdateCommand,
        clip_repository=clip_repository,
    )

    clip_retrieve_by_id_query = providers.Factory(
        ClipRetrieveQuery,
        clip_repository=clip_repository,
    )

    clip_list_query = providers.Factory(
        ClipListQuery,
        clip_repository=clip_repository,
    )

    management_list_query = providers.Factory(
        ClipManagementListQuery,
        query=clip_list_query,
    )

    like_the_clip_command = providers.Factory(
        LikeTheClipCommand,
        clip_like_repository=clip_like_repository,
        clip_retrieve_by_id_query=clip_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        clip_repository=clip_repository,
    )
