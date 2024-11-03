from contextlib import asynccontextmanager

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Header, status

from app.containers import Container
from app.domain.users.profile import schemas
from app.domain.users.core.schemas import StaffDetails, UserDetails
from app.domain.users.profile.commands import UserProfilePartialUpdateCommand
from app.domain.users.profile.queries import UserProfileMeQuery

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.get(
    "/me",
    response_model=UserDetails,
)
@wiring.inject
async def get_me(
        token: str = Header(...),
        query: UserProfileMeQuery = Depends(Provide[Container.user.profile_me_query]),
) -> StaffDetails:
    async with user_token(token):
        return await query()


@router.patch(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def update_profile(
        payload: schemas.UserProfilePartialUpdate,
        token: str = Header(...),
        command: UserProfilePartialUpdateCommand = Depends(
            wiring.Provide[Container.user.profile_partial_update_command]),
) -> None:
    async with user_token(token):
        return await command(payload)
