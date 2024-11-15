from uuid import UUID

from app.domain.news.repositories import NewsRepository, ReminderNewsRepository
from app.domain.news.schemas import NewsListRequestSchema
from app.domain.news import schemas

from a8t_tools.db.pagination import Paginated


class NewsListQuery:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def __call__(self, payload: schemas.NewsListRequestSchema) -> Paginated[schemas.News]:
        return await self.news_repository.get_news(payload.pagination, payload.sorting)


class NewsManagementListQuery:
    def __init__(self, query: NewsListQuery) -> None:
        self.query = query

    async def __call__(self, payload: NewsListRequestSchema) -> Paginated[schemas.News]:
        return await self.query(payload)


class NewsRetrieveQuery:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def __call__(self, news_id: UUID) -> schemas.NewsDetailsFull:
        news_result = await self.news_repository.get_news_by_filter_or_none(schemas.NewsWhere(id=news_id))
        return schemas.NewsDetailsFull.model_validate(news_result)


class TaskNewsRetrieveQuery:
    def __init__(self, reminder_news_repository: ReminderNewsRepository):
        self.reminder_news_repository = reminder_news_repository

    async def __call__(self, news_id: UUID, user_id: UUID) -> schemas.ReminderDetailsFull:
        print("Передалось user_id: ", user_id)
        print("Передалось news_id: ", news_id)

        task_id_news_result = await self.reminder_news_repository.get_task_id_news_by_filter_or_none(
            schemas.TaskIdNewsWhere(news_id=news_id, user_id=user_id))

        return schemas.ReminderDetailsFull.model_validate(task_id_news_result)
