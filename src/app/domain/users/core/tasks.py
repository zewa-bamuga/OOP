import asyncio
from typing import Any

from celery import current_task
from dependency_injector import wiring

from app.containers import Container
from app.domain.common.enums import TaskNames
from app.domain.common.schemas import IdContainer
from app.domain.news.repositories import ReminderNewsRepository
from app.domain.news.schemas import TaskIdCreate
from app.domain.users.core.commands import UserActivateCommand, EmailSenderCommand
from a8t_tools.bus.consumer import consume

from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)
user_timezone = timezone(timedelta(hours=7))


@consume(TaskNames.activate_user)
@wiring.inject
async def activate_user(
        user_id_container_dict: dict[str, Any],
        activate_user: UserActivateCommand = wiring.Provide[Container.user.activate_command],
) -> None:
    user_id_container = IdContainer.model_validate(user_id_container_dict)
    task_id = current_task.request.id
    logger.info(f"Task ID: {task_id}")
    await activate_user(user_id_container.id)


@consume(TaskNames.reminder_news)
@wiring.inject
async def reminder_news(
        reminder_id_container_dict: dict[str, Any],
        reminder_news: EmailSenderCommand = wiring.Provide[Container.user.email_sender_command],
        reminder_news_repository: ReminderNewsRepository = wiring.Provide[Container.news.reminder_news_repository],
        execution_time: str | None = None
) -> None:
    reminder_id_container = IdContainer.model_validate(reminder_id_container_dict)

    task_id = current_task.request.id

    print("Сейчас будет запись в таблицу")
    # Немедленно записываем task_id в базу данных
    await reminder_news_repository.create_task_id(
        reminder_id_container.id,
        TaskIdCreate(task_id=task_id)
    )

    print("Сейчас будет назначаться задача")
    # Создаем задачу для асинхронного выполнения
    if execution_time:
        scheduled_time = datetime.fromisoformat(execution_time).astimezone(user_timezone)
        current_time = datetime.now(user_timezone)

        delay = (scheduled_time - current_time).total_seconds()

        logger.info(f"Уведомление запланировано на отправку в {scheduled_time.isoformat()} (ваш часовой пояс)")

        if delay > 0:
            # Можно добавить задачу в asyncio для параллельного выполнения
            asyncio.create_task(wait_and_send_notification(scheduled_time, reminder_news, task_id))

    else:
        # Если execution_time нет, сразу вызываем отправку уведомления
        await reminder_news(task_id)


async def wait_and_send_notification(scheduled_time: datetime, reminder_news: EmailSenderCommand, task_id: str) -> None:
    # Ждем до запланированного времени
    delay = (scheduled_time - datetime.now(user_timezone)).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    logger.info(f"Отправка уведомления в {datetime.now(user_timezone).isoformat()} (ваш часовой пояс)")
    await reminder_news(task_id)
