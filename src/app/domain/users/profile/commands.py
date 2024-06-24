from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.core.commands import UserPartialUpdateCommand
from app.domain.users.core.schemas import UserPartialUpdateFull
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService
from app.domain.users.profile.schemas import UserProfilePartialUpdate


class UserProfilePartialUpdateCommand:
    def __init__(
        self,
        permission_service: UserPermissionService,
        current_user_query: CurrentUserQuery,
        user_partial_update_command: UserPartialUpdateCommand,
    ) -> None:
        self.permission_service = permission_service
        self.current_user_query = current_user_query
        self.user_partial_update_command = user_partial_update_command

    async def __call__(self, payload: UserProfilePartialUpdate) -> None:
        await self.permission_service.assert_permissions(BasePermissions.authenticated)
        current_user = await self.current_user_query()
        await self.user_partial_update_command(
            current_user.id, UserPartialUpdateFull(**payload.model_dump(exclude_unset=True))
        )
