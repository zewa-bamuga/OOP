import pytest

from tests import utils


@utils.async_methods_in_db_transaction
class TestVK:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_vk_subscribes(self):
        response = await self.client.get("/api/vk/v1/get")
        assert response.status_code == 200, response.json()
