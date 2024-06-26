from contextlib import asynccontextmanager

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Header

from app.containers import Container
from app.domain.users.core.schemas import UserDetails
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
) -> UserDetails:
    async with user_token(token):
        return await query()
