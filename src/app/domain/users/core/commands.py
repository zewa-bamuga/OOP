from uuid import UUID

from a8t_tools.security.hashing import PasswordHashService
from loguru import logger

from app.domain.common import enums
from app.domain.common.models import PasswordResetCode
from app.domain.users.core import schemas
from app.domain.users.core.queries import UserRetrieveByEmailQuery, UserRetrieveByCodeQuery
from app.domain.users.core.repositories import UserRepository, UpdatePasswordRepository, StaffRepository
from app.domain.users.core.schemas import UpdatePasswordRequest
from app.domain.users.registration.hi import send_password_reset_email


class UpdatePasswordRequestCommand:
    def __init__(
            self,
            user_retrieve_by_email_query: UserRetrieveByEmailQuery,
            repository: UpdatePasswordRepository,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.repository = repository

    async def __call__(self, payload: schemas.UpdatePasswordRequest) -> UpdatePasswordRequest:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)

        user_id = user_internal.id
        code = PasswordResetCode.generate_code()
        password_reset_code = schemas.PasswordResetCode(
            user_id=user_id,
            code=code,
        )

        await self.repository.delete_code(user_id)

        password_reset_code_id_container = await self.repository.create_update_password(password_reset_code)
        await send_password_reset_email(email, code)
        logger.info("Password reset code created: {password_reset_code_id}",
                    password_reset_code_id=password_reset_code_id_container.id)

        return UpdatePasswordRequest(email=email)


class UserPartialUpdateCommand:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> schemas.UserDetailsFull:
        await self.repository.partial_update_user(user_id, payload)
        user = await self.repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))
        assert user
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
        user_internal = await self.user_retrieve_by_email_query(email)

        code = payload.code
        code_internal = await self.user_retrieve_by_code_query(code)

        user_id = user_internal.id
        user_id_by_code = code_internal.user_id

        password_hash = await self.password_hash_service.hash(payload.password)

        update_payload = schemas.UserPartialUpdateFull(
            password_hash=password_hash
        )

        await self.user_partial_update_command(user_id, update_payload)

        print("user_id: ", user_id, "\nupdate_payload: ", update_payload)


class UserCreateCommand:
    def __init__(
            self,
            user_repository: UserRepository,
            staff_repository: StaffRepository,
    ):
        self.user_repository = user_repository
        self.staff_repository = staff_repository

    async def __call__(self, payload: schemas.StaffCreate) -> schemas.StaffDetails:
        if payload.permissions == {'employee'}:
            employee_id_container = await self.staff_repository.create_employee(
                schemas.StaffCreateFull(
                    status=enums.UserStatuses.unconfirmed,
                    **payload.model_dump(),
                )
            )
            logger.info(f"Employee created: {employee_id_container.id}")
            user = await self.staff_repository.get_employee_by_filter_or_none(schemas.UserWhere(id=employee_id_container.id))
            assert user
        else:
            user_id_container = await self.user_repository.create_user(
                schemas.UserCreateFull(
                    status=enums.UserStatuses.unconfirmed,
                    **payload.model_dump(),
                )
            )
            logger.info(f"User created: {user_id_container.id}")
            user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id_container.id))
            assert user

        return schemas.UserDetails.model_validate(user)


class UserActivateCommand:
    def __init__(
            self,
            repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)
