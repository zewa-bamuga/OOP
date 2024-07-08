from uuid import UUID

from a8t_tools.db.pagination import Paginated
from pydantic import EmailStr

from app.domain.common.exceptions import NotFoundError
from app.domain.users.core import schemas
from app.domain.users.core.repositories import UserRepository, UpdatePasswordRepository, StaffRepository


class UserListQuery:
    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    async def __call__(self, payload: schemas.StaffListRequestSchema) -> Paginated[schemas.Staff]:
        return await self.staff_repository.get_employee(payload.pagination, payload.sorting)


class StaffListQuery:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    async def __call__(self, payload: schemas.StaffListRequestSchema) -> Paginated[schemas.Staff]:
        return await self.repository.get_employee(payload.pagination, payload.sorting)


class UserRetrieveQuery:
    def __init__(self, user_repository: UserRepository, staff_repository: StaffRepository):
        self.user_repository = user_repository
        self.staff_repository = staff_repository

    async def __call__(self, user_id: UUID) -> schemas.UserInternal:
        try:
            user_result = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))
            if user_result:
                return schemas.UserInternal.model_validate(user_result)

            staff_result = await self.staff_repository.get_employee_by_filter_or_none(schemas.UserWhere(id=user_id))
            if staff_result:
                return schemas.UserInternal.model_validate(staff_result)

            raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при поиске пользователя и сотрудника:", e)
            raise


class EmailRetrieveQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_email: str) -> schemas.UserInternal:
        print("вошло в поиск по email:", user_email)

        result = await self.repository.get_user_by_filter_by_email_or_none((schemas.UserWhere(email=user_email)))
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class UserRetrieveByUsernameQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, firstname: str) -> schemas.UserInternal | None:
        return await self.repository.get_user_by_filter_or_none(schemas.UserWhere(firstname=firstname))


class UserRetrieveByEmailQuery:
    def __init__(self, user_repository: UserRepository, staff_repository: StaffRepository):
        self.user_repository = user_repository
        self.staff_repository = staff_repository

    async def __call__(self, email: str) -> schemas.UserInternal | None:
        print("Выполняется UserRetrieveByEmailQuery: ")
        try:
            user_internal = await self.user_repository.get_user_by_filter_by_email_or_none(
                schemas.UserWhere(email=email))
        except Exception as e:
            print("не попал:", e)
            user_internal = None

        if user_internal is None:
            user_internal = await self.staff_repository.get_staff_by_filter_by_email_or_none(
                schemas.UserWhere(email=email))

        return user_internal


class UserRetrieveByCodeQuery:
    def __init__(self, update_password_repository: UpdatePasswordRepository, staff_repository: StaffRepository):
        self.update_password_repository = update_password_repository
        self.staff_repository = staff_repository

    async def __call__(self, code: str) -> schemas.PasswordResetCode:
        password_reset_code_internal = await self.update_password_repository.get_password_reset_code_by_code_or_none(
            schemas.PasswordResetCodeWhere(code=code))

        if password_reset_code_internal is None:
            password_reset_code_internal = await self.staff_repository.get_password_reset_code_by_code_or_none(
                schemas.PasswordResetCodeWhere(code=code))

        print("выполняется после password_reset_code_internal")

        return password_reset_code_internal
