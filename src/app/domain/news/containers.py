from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction

from app.domain.news.commands import NewsCreateCommand, NewsPartialUpdateCommand, LikeTheNewsCommand, \
    UnlikeTheNewsCommand, ReminderTheNewsCommand, DeleteReminderTheNewsCommand, NewsDeleteCommand
from app.domain.news.queries import NewsRetrieveQuery, NewsManagementListQuery, NewsListQuery, TaskNewsRetrieveQuery
from app.domain.news.repositories import NewsRepository, LikeNewsRepository, ReminderNewsRepository
from app.domain.users.containers import UserContainer


class NewsContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    news_repository = providers.Factory(NewsRepository, transaction=transaction)

    news_like_repository = providers.Factory(LikeNewsRepository, transaction=transaction)
    reminder_news_repository = providers.Factory(ReminderNewsRepository, transaction=transaction)

    active_tasks = {}

    user_container = providers.Container(UserContainer)

    create_command = providers.Factory(
        NewsCreateCommand,
        news_repository=news_repository,
    )

    current_news_query = providers.Factory(
        NewsRetrieveQuery,
        news_repository=news_repository
    )

    news_partial_update_command = providers.Factory(
        NewsPartialUpdateCommand,
        news_repository=news_repository,
    )

    news_retrieve_by_id_query = providers.Factory(
        NewsRetrieveQuery,
        news_repository=news_repository,
    )

    news_list_query = providers.Factory(
        NewsListQuery,
        news_repository=news_repository,
    )

    management_list_query = providers.Factory(
        NewsManagementListQuery,
        query=news_list_query,
    )

    task_news_query = providers.Factory(
        TaskNewsRetrieveQuery,
        reminder_news_repository=reminder_news_repository,
    )

    delete_news = providers.Factory(
        NewsDeleteCommand,
        news_repository=news_repository,
    )

    reminder_the_news_command = providers.Factory(
        ReminderTheNewsCommand,
        news_retrieve_by_id_query=news_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        news_repository=news_repository,
        reminder_news_repository=reminder_news_repository,
        task_producer=user_container.task_producer,
    )

    delete_reminder_the_news_command = providers.Factory(
        DeleteReminderTheNewsCommand,
        news_retrieve_by_id_query=news_retrieve_by_id_query,
        task_news_query=task_news_query,
        current_user_query=user_container.current_user_query,
        news_repository=news_repository,
        reminder_news_repository=reminder_news_repository,
        task_producer=user_container.task_producer,
        active_tasks=active_tasks,
    )

    like_the_news_command = providers.Factory(
        LikeTheNewsCommand,
        news_like_repository=news_like_repository,
        news_retrieve_by_id_query=news_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        news_repository=news_repository,
    )

    unlike_the_news_command = providers.Factory(
        UnlikeTheNewsCommand,
        news_like_repository=news_like_repository,
        news_retrieve_by_id_query=news_retrieve_by_id_query,
        current_user_query=user_container.current_user_query,
        news_repository=news_repository,
    )
