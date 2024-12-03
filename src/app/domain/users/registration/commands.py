from a8t_tools.security.hashing import PasswordHashService

from app.domain.common.models import EmailCode
from app.domain.notifications.commands import EmailSender
from app.domain.users.core import schemas
from app.domain.users.core.commands import UserCreateCommand
from app.domain.users.core.repositories import EmailRpository
from app.domain.users.core.schemas import (
    EmailForCode,
    UserCreate,
    UserCredentialsRegist,
    UserDetails,
    VerificationCode,
)
from app.domain.users.permissions.schemas import BasePermissions


class UserEmailVerificationRequestCommand:
    def __init__(
        self,
        repository: EmailRpository,
        email_notification: EmailSender,
    ) -> None:
        self.repository = repository
        self.email_notification = email_notification

    async def __call__(self, payload: EmailForCode) -> None:
        email = payload.email
        code = EmailCode.generate_code()

        create_verification_code = schemas.EmailVerificationCode(
            email=email,
            code=code,
        )

        await self.repository.email_deletion(email)
        await self.repository.create_code(create_verification_code)
        await self.email_notification.send_verification_email(email, code)


class UserEmailVerificationConfirmCommand:
    def __init__(
        self,
        email_repository: EmailRpository,
    ) -> None:
        self.email_repository = email_repository

    async def __call__(self, payload: VerificationCode) -> None:
        code = payload.code
        email = payload.email

        email_confirm = await self.email_repository.code_deletion(code)

        if email == email_confirm:
            return True
        else:
            return False


class UserRegisterCommand:
    def __init__(
        self,
        create_command: UserCreateCommand,
        password_hash_service: PasswordHashService,
        email_notification: EmailSender,
    ) -> None:
        self.create_command = create_command
        self.password_hash_service = password_hash_service
        self.email_notification = email_notification

    async def __call__(self, payload: UserCredentialsRegist) -> UserDetails:
        user_create = await self.create_command(
            UserCreate(
                firstname=payload.firstname,
                lastname=payload.lastname,
                email=payload.email,
                password_hash=(await self.password_hash_service.hash(payload.password)),
                avatar_attachment_id=None,
                permissions={BasePermissions.user},
            )
        )

        await self.email_notification.send_first_registration(user_create.email)
        return user_create
