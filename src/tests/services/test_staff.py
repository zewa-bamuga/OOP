from app.domain.common import enums
from app.containers import Container
from app.domain.users.core import schemas
from app.domain.users.staff.schemas import StaffInternal

from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestStaff:
    async def test_list(self, container: Container):
        factories.StaffFactory.create_batch(10)
        results = await container.user.staff_list_query()(
            schemas.StaffListRequestSchema()
        )
        assert len(results.items) == 10
        assert isinstance(results.items[0], schemas.Staff)

    async def test_retrieve(self, container: Container):
        staff = factories.StaffFactory.create()
        results = await container.user.staff_retrieve_by_id_query()(staff.id)
        assert isinstance(results, StaffInternal)