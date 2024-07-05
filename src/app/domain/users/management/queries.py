from uuid import UUID

from app.domain.users.core.queries import UserListQuery, UserRetrieveQuery, EmailRetrieveQuery
from app.domain.users.core.schemas import User, UserDetailsFull, UserListRequestSchema, StaffListRequestSchema
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService
from a8t_tools.db.pagination import Paginated


class UserManagementListQuery:
    def __init__(self, permission_service: UserPermissionService, query: UserListQuery) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: StaffListRequestSchema) -> Paginated[User]:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        return await self.query(payload)


class UserManagementRetrieveQuery:
    def __init__(
            self,
            query: UserRetrieveQuery,
            permission_service: UserPermissionService,
    ) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: UUID) -> UserDetailsFull:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        user = await self.query(payload)
        return UserDetailsFull.model_validate(user)

#
# class EmailManagementRetrieveQuery:
#     def __init__(
#             self,
#             query: EmailRetrieveQuery,
#     ) -> None:
#         self.query = query
#
#     async def __call__(self, payload: str) -> UserDetailsFull:
#         await self.permission_service.assert_permissions(BasePermissions.superuser)
#         email = await self.query(payload)
#         return UserDetailsFull.model_validate(email)
