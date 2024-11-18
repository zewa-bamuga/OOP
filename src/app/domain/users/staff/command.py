from uuid import UUID

from app.domain.users.core.repositories import StaffRepository
from app.domain.users.staff import schemas
from app.domain.users.staff.schemas import StaffCreate


class StaffCreateCommand:
    def __init__(
            self,
            staff_repository: StaffRepository,
    ) -> None:
        self.staff_repository = staff_repository

    async def __call__(self, payload: StaffCreate) -> None:
        staff_create_data = schemas.StaffCreate(
            firstname=payload.firstname,
            lastname=payload.lastname,
            email=payload.email,
            qualification=payload.qualification,
            post=payload.post,
            description=payload.description,
            link_to_vk=payload.link_to_vk,
        )

        staff_id_container = await self.staff_repository.create_employee(staff_create_data)

        staff = await self.staff_repository.get_employee_by_filter_or_none(
            schemas.StaffWhere(id=staff_id_container.id)
        )

        assert staff

        return schemas.StaffDetails.model_validate(staff)


class StaffDeleteCommand:
    def __init__(self, staff_repository: StaffRepository) -> None:
        self.staff_repository = staff_repository

    async def __call__(self, payload: schemas.StaffDelete) -> None:
        return await self.staff_repository.delete_staff(payload.id)
