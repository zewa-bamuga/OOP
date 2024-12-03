import pytest

from app.domain.common import enums
from app.domain.users.core.tasks import activate_user
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestUsers:
    @pytest.fixture(autouse=True)
    def setup(self, client) -> None:
        self.client = client

    async def test_activate_user(self, fs):
        filename = "/test"
        fs.create_file(f"/media{filename}", contents="test")
        user = factories.UserFactory.create(
            status=enums.UserStatuses.unconfirmed,
            avatar_attachment__path=filename,
        )
        await activate_user(dict(id=user.id))
        assert user.status == enums.UserStatuses.active
