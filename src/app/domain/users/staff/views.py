from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, Header

from app.api import deps
from app.containers import Container
from app.domain.users.management.queries import UserManagementListQuery
from app.domain.users.core import schemas

from a8t_tools.db import pagination, sorting

from app.domain.users.staff.command import StaffCreateCommand
from app.domain.users.staff.queries import StaffRetrieveQuery
from app.domain.users.staff.schemas import StaffCreate

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.get(
    "/get",
    response_model=pagination.CountPaginationResults[schemas.Staff],
)
@wiring.inject
async def get_staff_list(
        token: str = Header(...),
        query: UserManagementListQuery = Depends(wiring.Provide[Container.user.management_list_query]),
        pagination: pagination.PaginationCallable[schemas.Staff] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.Staff)),
        sorting: sorting.SortingData[schemas.StaffSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.StaffSorts,
                schemas.StaffSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.Staff]:
    async with user_token(token):
        return await query(schemas.StaffListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/get/by/id/{staff_id}",
    response_model=None
)
@wiring.inject
async def get_staff_by_id(
        staff_id: UUID,
        query: StaffRetrieveQuery = Depends(wiring.Provide[Container.user.staff_retrieve_by_id_query]),
):
    return await query(staff_id)


@router.post(
    "/create",
    response_model=schemas.Staff
)
@wiring.inject
async def create_staff(
        payload: StaffCreate,
        token: str = Header(...),
        command: StaffCreateCommand = Depends(wiring.Provide[Container.user.staff_create]),
) -> schemas.StaffDetails:
    async with user_token(token):
        return await command(payload)
