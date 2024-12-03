from uuid import UUID

from app.domain.users.core.repositories import StaffRepository
from app.domain.users.staff import schemas


class StaffRetrieveQuery:
    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    async def __call__(self, staff_id: UUID) -> schemas.StaffDetails:
        staff_result = await self.staff_repository.get_employee_by_filter_or_none(
            schemas.StaffWhere(id=staff_id)
        )
        return schemas.StaffDetails.model_validate(staff_result)
