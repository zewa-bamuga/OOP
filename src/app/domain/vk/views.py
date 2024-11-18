from dependency_injector import wiring
from fastapi import APIRouter

from app.domain.vk.commands import get_vk_followers_count

router = APIRouter()


@router.get(
    "/get",
    response_model=None
)
@wiring.inject
async def get_followers_count():
    return await get_vk_followers_count()
