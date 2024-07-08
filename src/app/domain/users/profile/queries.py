from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.core.schemas import UserDetails, StaffDetails
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService


class UserProfileMeQuery:
    def __init__(
        self,
        permission_service: UserPermissionService,
        current_user_query: CurrentUserQuery,
    ) -> None:
        self.permission_service = permission_service
        self.current_user_query = current_user_query

    async def __call__(self) -> StaffDetails:
        print("Выполняется UserProfileMeQuery")
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        print("Выполняется между UserProfileMeQuery")
        return await self.current_user_query()
