from email.message import EmailMessage
from uuid import UUID
import smtplib

from a8t_tools.bus.producer import TaskProducer
from a8t_tools.security.hashing import PasswordHashService
from loguru import logger

from app.domain.common import enums
from app.domain.common.exceptions import NotFoundError
from app.domain.common.models import PasswordResetCode
from app.domain.common.schemas import IdContainer
from app.domain.notifications.commands import EmailSender
from app.domain.projects.repositories import ProjectRepository
from app.domain.users.core import schemas
from app.domain.users.core.queries import UserRetrieveByEmailQuery, UserRetrieveByCodeQuery
from app.domain.users.core.repositories import UserRepository, UpdatePasswordRepository, StaffRepository
from app.domain.users.core.schemas import EmailForCode


class UpdatePasswordRequestCommand:
    def __init__(
            self,
            user_retrieve_by_email_query: UserRetrieveByEmailQuery,
            repository: UpdatePasswordRepository,
            email_notification: EmailSender,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.repository = repository
        self.email_notification = email_notification

    async def __call__(self, payload: schemas.EmailForCode) -> EmailForCode:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)

        user_id = user_internal.id
        code = PasswordResetCode.generate_code()

        password_reset_code = schemas.PasswordResetCode(
            user_id=user_id,
            code=code,
        )

        await self.repository.delete_code(user_id)
        await self.repository.create_update_password(password_reset_code)
        await self.email_notification.send_password_reset_email(email, code)

        return EmailForCode(email=email)


class UserPartialUpdateCommand:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> schemas.UserDetailsFull:
        try:
            await self.user_repository.partial_update_user(user_id, payload)
            user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении пользователя или сотрудника:", e)
            raise

        return schemas.UserDetailsFull.model_validate(user)


class ProjectAvatarUpdateCommand:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def __call__(self, project_id: UUID, payload: schemas.UserPartialUpdate) -> schemas.UserDetailsFull:
        try:
            await self.project_repository.partial_update_project(project_id, payload)
            user = await self.project_repository.get_user_by_filter_or_none(schemas.UserWhere(id=project_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении пользователя или сотрудника:", e)
            raise

        return schemas.UserDetailsFull.model_validate(user)


class UpdatePasswordConfirmCommand:
    def __init__(
            self,
            user_retrieve_by_email_query: UserRetrieveByEmailQuery,
            user_retrieve_by_code_query: UserRetrieveByCodeQuery,
            repository: UserRepository,
            user_partial_update_command: UserPartialUpdateCommand,
            password_hash_service: PasswordHashService,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.user_retrieve_by_code_query = user_retrieve_by_code_query
        self.repository = repository
        self.user_partial_update_command = user_partial_update_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: schemas.UpdatePasswordConfirm) -> None:
        email = payload.email
        print("выполняется user_retrieve_by_email_query")
        user_internal = await self.user_retrieve_by_email_query(email)
        print("выполняется user_internal: ", user_internal)

        print("выполняется user_retrieve_by_code_query")
        code = payload.code
        code_internal = await self.user_retrieve_by_code_query(code)
        print("после user_retrieve_by_code_query: ", code_internal)

        user_id = user_internal.id
        user_id_by_code = code_internal.user_id
        print("user_id: ", user_id)

        password_hash = await self.password_hash_service.hash(payload.password)

        update_payload = schemas.UserPartialUpdateFull(
            password_hash=password_hash
        )

        print("Сейчас будет передаваться в user_partial_update_command")

        await self.user_partial_update_command(user_id, update_payload)

        print("user_id: ", user_id, "\nupdate_payload: ", update_payload)


class UserCreateCommand:
    def __init__(
            self,
            user_repository: UserRepository,
            staff_repository: StaffRepository,
            task_producer: TaskProducer,
    ):
        self.user_repository = user_repository
        self.staff_repository = staff_repository
        self.task_producer = task_producer

    async def __call__(self, payload: schemas.StaffCreate) -> schemas.StaffDetails:
        if payload.permissions == {'employee'}:
            employee_id_container = await self.staff_repository.create_employee(
                schemas.StaffCreateFull(
                    status=enums.UserStatuses.unconfirmed,
                    **payload.model_dump(),
                )
            )
            logger.info(f"Employee created: {employee_id_container.id}")
            user = await self.staff_repository.get_employee_by_filter_or_none(
                schemas.UserWhere(id=employee_id_container.id))
            assert user
        else:
            user_id_container = await self.user_repository.create_user(
                schemas.UserCreateFull(
                    status=enums.UserStatuses.unconfirmed,
                    **payload.model_dump(),
                )
            )
            logger.info(f"User created: {user_id_container.id}")
            await self._enqueue_user_activation(user_id_container)
            user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id_container.id))
            assert user

        return schemas.UserDetails.model_validate(user)

    async def _enqueue_user_activation(self, user_id_container: IdContainer) -> None:
        await self.task_producer.fire_task(
            enums.TaskNames.activate_user,
            queue=enums.TaskQueues.main_queue,
            user_id_container_dict=user_id_container.json_dict(),
        )


class UserActivateCommand:
    def __init__(
            self,
            repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)


# Временно, я сейчас сделал класс для отправок писем. Эта часть на время, пока работаю с напоминаниями и тасками
class EmailSenderCommand:
    async def __call__(self, task_id: UUID) -> None:
        email_address = "tikhonov.igor2028@yandex.ru"
        email_password = "abqiulywjvibrefg"

        msg = EmailMessage()
        msg['Subject'] = "Напоминание о новости"
        msg['From'] = email_address
        msg['To'] = 'tikhonov.igor2028@yandex.ru'

        html_content = f"""\
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
                <h2 style="color: #FFD700;">Сброс пароля</h2>
                <p>Здравствуйте,</p>
                <p>Подтверждение почты на платформе Отдела Образовательных Программ.</p>
                <p>Код для подтверждения почты:</p>
                <p style="font-size: 18px; font-weight: bold; color: #FFD700;"></p>
                <p>Если вы не запрашивали подтверждения почты, проигнорируйте это письмо.</p>
                <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
                <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
            </div>
        </body>
        </html>
        """

        msg.set_content(
            f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля:\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
        )
        msg.add_alternative(html_content, subtype='html')

        with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
