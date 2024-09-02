from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction

from app.domain.clips.commands import ClipCreateCommand, ClipPartialUpdateCommand, LikeTheClipCommand
from app.domain.clips.queries import ClipRetrieveQuery
from app.domain.clips.repositories import ClipRepository
from app.domain.news.commands import NewsCreateCommand, NewsPartialUpdateCommand, LikeTheNewsCommand, \
    UnlikeTheNewsCommand
from app.domain.news.queries import NewsRetrieveQuery, NewsManagementListQuery, NewsListQuery
from app.domain.news.repositories import NewsRepository, LikeNewsRepository
from app.domain.users.containers import UserContainer


class ClipContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    clip_repository = providers.Factory(ClipRepository, transaction=transaction)

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

    like_the_news_command = providers.Factory(
        LikeTheClipCommand,
        news_like_repository=cl_like_repository,
        news_retrieve_by_id_query=news_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        news_repository=news_repository,
    )