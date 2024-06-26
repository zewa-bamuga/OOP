from app.domain.users.core.commands import UserCreateCommand
from app.domain.users.core.schemas import UserCreate, UserCredentials, UserDetails
from a8t_tools.security.hashing import PasswordHashService


class UserRegisterCommand:
    def __init__(
        self,
        user_create_command: UserCreateCommand,
        password_hash_service: PasswordHashService,
    ) -> None:
        self.user_create_command = user_create_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: UserCredentials) -> UserDetails:
        return await self.user_create_command(
            UserCreate(
                firstname=payload.firstname,
                email=payload.email,
                password_hash=(await self.password_hash_service.hash(payload.password)),
                avatar_attachment_id=None,
                permissions=set(),
            )
        )