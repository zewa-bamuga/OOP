from uuid import UUID

import sqlalchemy as sa
from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from sqlalchemy import ColumnElement, and_, select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models, enums
from app.domain.common.schemas import IdContainer, IdContainerTables
from app.domain.users.core import schemas


class EmailRpository(CrudRepositoryMixin[models.EmailCode]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.EmailCode
        self.transaction = transaction

    async def create_code(self, payload: schemas.EmailVerificationCode) -> IdContainerTables:
        return IdContainerTables(id=await self._create(payload))

    async def email_deletion(self, email: str) -> None:
        async with self.transaction.use() as session:
            check_query = select(models.EmailCode).where(models.EmailCode.email == email)
            result = await session.execute(check_query)
            email_exists = result.first()

            if email_exists:
                stmt = sa.delete(models.EmailCode).where(models.EmailCode.email == email)
                await session.execute(stmt)
                await session.commit()

    async def code_deletion(self, code: int) -> str:
        async with self.transaction.use() as session:
            check_query = select(models.EmailCode).where(models.EmailCode.code == code)
            result = await session.execute(check_query)
            email_exists = result.first()

            if email_exists:
                email = email_exists[0].email
                return email

            raise ValueError(f"Code {code} not found.")


class UpdatePasswordRepository(CrudRepositoryMixin[models.PasswordResetCode]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.PasswordResetCode
        self.transaction = transaction

    async def create_update_password(self, payload: schemas.PasswordResetCode) -> IdContainerTables:
        async with self.transaction.use() as session:
            try:
                staff_query = select(models.Staff).where(models.Staff.id == payload.user_id)
                staff_exists = await session.execute(staff_query)

                if staff_exists.first():
                    stmt = insert(models.PasswordResetCode).values(
                        {
                            "staff_id": payload.user_id,
                            "code": payload.code,
                        }
                    )
                else:
                    stmt = insert(models.PasswordResetCode).values(
                        {
                            "user_id": payload.user_id,
                            "code": payload.code,
                        }
                    )

                await session.execute(stmt)

            except Exception as e:
                print(f"Error creating code info: {e}")

    async def delete_code(self, user_id: UUID) -> None:
        async with self.transaction.use() as session:
            staff_query = select(models.Staff).where(models.Staff.id == user_id)
            staff_exists = await session.execute(staff_query)

            if staff_exists.first():
                stmt = sa.delete(models.PasswordResetCode).where(models.PasswordResetCode.staff_id == user_id)
            else:
                stmt = sa.delete(models.PasswordResetCode).where(models.PasswordResetCode.user_id == user_id)

            await session.execute(stmt)
            await session.commit()

    async def get_password_reset_code_by_code_or_none(self,
                                                      where: schemas.PasswordResetCodeWhere) -> schemas.PasswordResetCode:
        print("выполняется в get_password_reset_code_by_code_or_none")
        result = await self._get_or_none(
            schemas.PasswordResetCode,
            condition=await self._format_filters_code(where),
        )

        # Проверяем результат, если user_id не найден, ищем по staff_id
        if result is None and where.staff_id is not None:
            print("User ID not found, searching by Staff ID")
            result = await self._get_or_none(
                schemas.PasswordResetCode,
                condition=await self._format_filters_code_by_staff(where),
            )

        return result

    async def _format_filters_code(self, where: schemas.PasswordResetCodeWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []
        print("выполняется в _format_filters_code")

        if where.id is not None:
            print("выполняется поиск 1")
            filters.append(models.PasswordResetCode.id == where.id)

        if where.code is not None:
            print("выполняется поиск 2")
            filters.append(models.PasswordResetCode.code == where.code)
            print("выполняется поиск 2 конец")

        if where.user_id is not None:
            print("выполняется поиск по user_id")
            filters.append(models.PasswordResetCode.user_id == where.user_id)

        print("where.code: ", where.code)
        print("where.user_id: ", where.user_id)

        return and_(*filters)

    async def _format_filters_code_by_staff(self, where: schemas.PasswordResetCodeWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []
        print("выполняется в _format_filters_code_by_staff")

        if where.id is not None:
            print("выполняется поиск 1")
            filters.append(models.PasswordResetCode.id == where.id)

        if where.code is not None:
            print("выполняется поиск 2")
            filters.append(models.PasswordResetCode.code == where.code)
            print("выполняется поиск 2 конец")

        if where.staff_id is not None:
            print("выполняется поиск по staff_id")
            filters.append(models.PasswordResetCode.staff_id == where.staff_id)

        print("where.code: ", where.code)
        print("where.staff_id: ", where.staff_id)

        return and_(*filters)


class StaffRepository(CrudRepositoryMixin[models.Staff]):
    load_options: list[ExecutableOption] = [
        selectinload(models.Staff.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Staff
        self.transaction = transaction

    async def create_employee(self, payload: schemas.UserCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_employee(
            self,
            pagination: PaginationCallable[schemas.Staff] | None = None,
            sorting: SortingData[schemas.StaffSorts] | None = None,
    ) -> Paginated[schemas.Staff]:
        return await self._get_list(
            schemas.User,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def get_employee_by_filter_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters_email(where),
            options=self.load_options,
        )

    async def partial_update_staff(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> None:
        return await self._partial_update(user_id, payload)

    async def get_password_reset_code_by_code_or_none(self,
                                                      where: schemas.PasswordResetCodeWhere) -> schemas.PasswordResetCode | None:
        return await self._get_or_none(
            schemas.PasswordResetCode,
            condition=await self._format_filters_code(where),
        )

    async def get_staff_by_filter_by_email_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters_email(where),
            options=self.load_options,
        )

    async def _format_filters_email(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.Staff.id == where.id)

        if where.email is not None:
            filters.append(models.Staff.email == where.email)

        return and_(*filters)


class UserRepository(CrudRepositoryMixin[models.User]):
    load_options: list[ExecutableOption] = [
        selectinload(models.User.avatar_attachment),
    ]

    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.User
        self.transaction = transaction

    async def get_users(
            self,
            pagination: PaginationCallable[schemas.User] | None = None,
            sorting: SortingData[schemas.UserSorts] | None = None,
    ) -> Paginated[schemas.User]:
        return await self._get_list(
            schemas.User,
            pagination=pagination,
            sorting=sorting,
            options=self.load_options,
        )

    async def get_user_by_filter_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters(where),
            options=self.load_options,
        )

    async def get_user_by_filter_by_email_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters_email(where),
            options=self.load_options,
        )

    async def create_user(self, payload: schemas.UserCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def partial_update_user(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> None:
        return await self._partial_update(user_id, payload)

    async def delete_user(self, user_id: UUID) -> None:
        return await self._delete(user_id)

    async def set_user_status(self, user_id: UUID, status: enums.UserStatuses) -> None:
        return await self._partial_update(user_id, schemas.UserPartialUpdate(status=status))

    async def _format_filters(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.firstname is not None:
            filters.append(models.User.firstname == where.firstname)

        return and_(*filters)

    async def _format_filters_email(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.email is not None:
            filters.append(models.User.email == where.email)

        return and_(*filters)
