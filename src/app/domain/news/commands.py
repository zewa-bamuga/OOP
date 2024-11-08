import datetime
import smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from uuid import UUID

from a8t_tools.bus.producer import TaskProducer
from loguru import logger

from celery import shared_task
from fastapi import HTTPException

from app.domain.common import enums
from app.domain.common.exceptions import NotFoundError
from app.domain.common.schemas import IdContainer
from app.domain.news.queries import NewsRetrieveQuery
from app.domain.news.repositories import NewsRepository, LikeNewsRepository, ReminderNewsRepository
from app.domain.news.schemas import NewsCreate, ReminderTheNews
from app.domain.projects.schemas import Like
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.news import schemas


# @shared_task
# def send_news_reminder_email(user_email: str, news_name: str, news_description: str):
#     print("Выполняется celery")
#
#     subject = f"Напоминание о новости: {news_name}"
#     message = f"Не забудьте прочитать новость: {news_description}"
#
#     # Отправка email
#     send_email_reminder(user_email, subject, message)


async def send_email_reminder(to_email: str, subject: str, message: str):
    print("Выполняется Отправка на почту")

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'tikhonov.igor2028@yandex.ru'
    msg['To'] = to_email

    # Настройте SMTP-сервер
    with smtplib.SMTP('smtp.yandex.ru', 465) as server:
        server.starttls()
        server.login('tikhonov.igor2028@yandex.ru', 'abqiulywjvibrefg')
        server.send_message(msg)


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


class NewsPartialUpdateCommand:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    async def __call__(self, news_id: UUID, payload: schemas.NewsPartialUpdate) -> schemas.NewsDetailsFull:
        try:
            await self.news_repository.partial_update_news(news_id, payload)
            user = await self.news_repository.get_news_by_filter_or_none(schemas.NewsWhere(id=news_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении новости:", e)
            raise

        return schemas.NewsDetailsFull.model_validate(user)


class ReminderTheNewsCommand:
    def __init__(
            self,
            news_retrieve_by_id_query: NewsRetrieveQuery,
            current_user_query: CurrentUserQuery,
            news_repository: NewsRepository,
            reminder_news_repository: ReminderNewsRepository,
            task_producer: TaskProducer,
    ) -> None:
        self.news_retrieve_by_id_query = news_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.news_repository = news_repository
        self.reminder_news_repository = reminder_news_repository
        self.task_producer = task_producer

    async def __call__(self, payload: ReminderTheNews) -> None:
        news_id = payload.news_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        news = await self.news_retrieve_by_id_query(news_id)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")

        new_reminder_count = news.reminder + 1
        create_reminder_the_news = schemas.ReminderCreate(
            news_id=news_id,
            user_id=user_id,
        )
        reminder_id_container = await self.reminder_news_repository.create_reminder(create_reminder_the_news)

        await self.news_repository.update_news_reminder(news_id, new_reminder_count)

        logger.info(f"Reminder created: {reminder_id_container.id}")

        # Вычисляем время для уведомления (24 часа до события)
        notification_time = news.date - timedelta(days=1)

        # Запланируем задачу напоминания на указанное время
        await self._enqueue_news_reminder(reminder_id_container, notification_time)

    async def _enqueue_news_reminder(self, reminder_id_container: IdContainer, notification_time: datetime) -> None:
        print("Сейчас _enqueue_news_reminder")

        # Передаем время выполнения задачи
        task_id = await self.task_producer.fire_task(
            enums.TaskNames.reminder_news,
            queue=enums.TaskQueues.main_queue,
            reminder_id_container_dict=reminder_id_container.json_dict(),
            execution_time=notification_time.isoformat()
        )

        # Логируем task_id
        logger.info(f"Task ID создан и передан: {task_id}")

        print("В _enqueue_news_reminder task_id: ", task_id)
        await self.reminder_news_repository.save_task_id(reminder_id_container.id, task_id)


class LikeTheNewsCommand:
    def __init__(
            self,
            news_like_repository: LikeNewsRepository,
            news_retrieve_by_id_query: NewsRetrieveQuery,
            current_user_query: CurrentUserQuery,
            news_repository: NewsRepository
    ) -> None:
        self.news_like_repository = news_like_repository
        self.news_retrieve_by_id_query = news_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.news_repository = news_repository

    async def __call__(self, payload: Like) -> None:
        news_id = payload.news_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        news = await self.news_retrieve_by_id_query(news_id)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")

        like_exists = await self.news_like_repository.check_like_exists(news_id, user_id)

        if like_exists:
            new_likes_count = news.likes - 1
            await self.news_like_repository.delete_like_news(news_id, user_id)
        else:
            new_likes_count = news.likes + 1
            create_like_the_news = schemas.LikeTheNews(
                news_id=news_id,
                user_id=user_id,
            )
            await self.news_like_repository.create_like_news(create_like_the_news)

        await self.news_repository.update_news_likes(news_id, new_likes_count)


class UnlikeTheNewsCommand:
    def __init__(
            self,
            news_like_repository: LikeNewsRepository,
            news_retrieve_by_id_query: NewsRetrieveQuery,
            current_user_query: CurrentUserQuery,
            news_repository: NewsRepository
    ) -> None:
        self.news_like_repository = news_like_repository
        self.news_retrieve_by_id_query = news_retrieve_by_id_query
        self.current_user_query = current_user_query
        self.news_repository = news_repository

    async def __call__(self, payload: Like) -> None:
        news_id = payload.news_id
        current_user = await self.current_user_query()
        user_id = current_user.id

        news = await self.news_retrieve_by_id_query(news_id)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")

        like_exists = await self.news_like_repository.check_like_exists(news_id, user_id)
        if not like_exists:
            raise HTTPException(status_code=404, detail="Like not found")

        new_likes_count = max(news.likes - 1, 0)

        await self.news_like_repository.delete_like_news(news_id, user_id)
        await self.news_repository.update_news_likes(news_id, new_likes_count)
