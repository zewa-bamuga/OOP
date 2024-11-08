import asyncio
from typing import Any

from celery import current_task
from dependency_injector import wiring

from app.containers import Container
from app.domain.common.enums import TaskNames
from app.domain.common.schemas import IdContainer
from app.domain.users.core.commands import UserActivateCommand, EmailSenderCommand
from a8t_tools.bus.consumer import consume

from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)


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


user_timezone = timezone(timedelta(hours=7))


@consume(TaskNames.reminder_news)
@wiring.inject
async def reminder_news(
        reminder_id_container_dict: dict[str, Any],
        reminder_news: EmailSenderCommand = wiring.Provide[Container.user.email_sender_command],
        execution_time: str | None = None
) -> None:
    reminder_id_container = IdContainer.model_validate(reminder_id_container_dict)

    # Получаем идентификатор текущей задачи
    task_id = current_task.request.id
    logger.info(f"Task ID: {task_id}")

    if execution_time:
        # Преобразуем `execution_time` в нужный часовой пояс
        scheduled_time = datetime.fromisoformat(execution_time).astimezone(user_timezone)
        current_time = datetime.now(user_timezone)

        delay = (scheduled_time - current_time).total_seconds()

        # Логируем запланированное время отправки в вашем часовом поясе
        logger.info(f"Уведомление запланировано на отправку в {scheduled_time.isoformat()} (ваш часовой пояс)")
        logger.info(f"Task ID: {task_id}")
        logger.info(f"Task ID_dict: {reminder_id_container_dict}")

        if delay > 0:
            await asyncio.sleep(delay)  # Ждем до назначенного времени

    # Логируем фактическое время отправки в вашем часовом поясе
    logger.info(f"Отправка уведомления в {datetime.now(user_timezone).isoformat()} (ваш часовой пояс)")
    logger.info(f"Task ID: {task_id}")

    await reminder_news()

    # Логируем task_id
