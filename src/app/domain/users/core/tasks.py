from typing import Any

from dependency_injector import wiring

from app.containers import Container
from app.domain.common.enums import TaskNames
from app.domain.common.schemas import IdContainer
from app.domain.users.core.commands import UserActivateCommand, EmailSenderCommand
from a8t_tools.bus.consumer import consume


@consume(TaskNames.activate_user)
@wiring.inject
async def activate_user(
        user_id_container_dict: dict[str, Any],
        activate_user: UserActivateCommand = wiring.Provide[Container.user.activate_command],
) -> None:
    user_id_container = IdContainer.model_validate(user_id_container_dict)
    await activate_user(user_id_container.id)


@consume(TaskNames.reminder_news)
@wiring.inject
async def reminder_news(
        reminder_id_container_dict: dict[str, Any],
        reminder_news: EmailSenderCommand = wiring.Provide[Container.user.email_sender_command],
        execution_time: str | None = None,  # добавьте этот параметр
) -> None:
    reminder_id_container = IdContainer.model_validate(reminder_id_container_dict)

    # Вы можете использовать execution_time здесь, если это необходимо
    if execution_time:
        # Логика обработки времени, если нужно
        print(f"Напоминание будет отправлено в {execution_time}")

    await reminder_news()
