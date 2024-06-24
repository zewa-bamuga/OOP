from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.containers import Container
from app.domain.users.core.schemas import UserCredentials, UserDetails
from app.domain.users.registration.commands import UserRegisterCommand
from app.domain.users.registration.hi import send_hello

router = APIRouter()


@router.post(
    "/registration",
    response_model=UserDetails,
)
@wiring.inject
async def register(
    payload: UserCredentials,
    command: UserRegisterCommand = Depends(wiring.Provide[Container.user.register_command]),
) -> UserDetails:
    user_details = await command(payload)
    await send_hello(user_details)
    return user_details
