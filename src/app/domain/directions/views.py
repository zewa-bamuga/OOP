from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.api import deps
from app.containers import Container
from app.domain.news.queries import NewsManagementListQuery
from app.domain.news import schemas

from a8t_tools.db import pagination, sorting

router = APIRouter()


@router.get(
    "/get",
    response_model=pagination.CountPaginationResults[schemas.NewsDetailsFull],
)
@wiring.inject
async def get_directions_list(
        query: NewsManagementListQuery = Depends(wiring.Provide[Container.news.management_list_query]),
        pagination: pagination.PaginationCallable[schemas.NewsDetailsFull] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.NewsDetailsFull)),
        sorting: sorting.SortingData[schemas.NewsSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.NewsSorts,
                schemas.NewsSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.NewsDetailsFull]:
    return await query(schemas.NewsListRequestSchema(pagination=pagination, sorting=sorting))
