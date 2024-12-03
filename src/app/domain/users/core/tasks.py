import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from a8t_tools.bus.consumer import consume
from celery import current_task
from dependency_injector import wiring

from app.containers import Container
from app.domain.common.enums import TaskNames
from app.domain.common.schemas import IdContainer
from app.domain.news.repositories import ReminderNewsRepository
from app.domain.news.schemas import TaskIdCreate
from app.domain.users.core.commands import EmailSenderCommand, UserActivateCommand

logger = logging.getLogger(__name__)
user_timezone = timezone(timedelta(hours=7))


@consume(TaskNames.activate_user)
@wiring.inject
async def activate_user(
    user_id_container_dict: dict[str, Any],
    activate_user: UserActivateCommand = wiring.Provide[
        Container.user.activate_command
    ],
) -> None:
    user_id_container = IdContainer.model_validate(user_id_container_dict)
    await activate_user(user_id_container.id)


@consume(TaskNames.reminder_news)
@wiring.inject
async def reminder_news(
    reminder_id_container_dict: dict[str, Any],
    reminder_news: EmailSenderCommand = wiring.Provide[
        Container.user.email_sender_command
    ],
    reminder_news_repository: ReminderNewsRepository = wiring.Provide[
        Container.news.reminder_news_repository
    ],
    execution_time: str | None = None,
) -> None:
    reminder_id_container = IdContainer.model_validate(reminder_id_container_dict)

    task_id = current_task.request.id

    await reminder_news_repository.create_task_id(
        reminder_id_container.id, TaskIdCreate(task_id=task_id)
    )

    if execution_time:
        scheduled_time = datetime.fromisoformat(execution_time).astimezone(
            user_timezone
        )
        current_time = datetime.now(user_timezone)

        delay = (scheduled_time - current_time).total_seconds()

        if delay > 0:
            asyncio.create_task(
                wait_and_send_notification(scheduled_time, reminder_news, task_id)
            )

    else:
        await reminder_news(task_id)


async def wait_and_send_notification(
    scheduled_time: datetime, reminder_news: EmailSenderCommand, task_id: str
) -> None:
    delay = (scheduled_time - datetime.now(user_timezone)).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    await reminder_news(task_id)
