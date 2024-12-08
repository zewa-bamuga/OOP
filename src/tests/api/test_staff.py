import pytest

from app.domain.users.auth import schemas
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestStaff:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_staff_create(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        response = await self.client.post(
            "/api/staff/v1/create",
            json=dict(
                firstname="test_firstname",
                lastname="test_lastname",
                email="test@mail.ru",
                qualification="test_qualification",
                post="test_post",
                description="test_description",
                link_to_vk="test_link_to_vk",
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()

    # async def test_staff_list(self, token_data_factory):
    #     user = factories.UserFactory.create()
    #     tokens: schemas.TokenResponse = await token_data_factory(user)
    #
    #     factories.StaffFactory.create_batch(10)
    #
    #     response = await self.client.get(
    #         "/api/staff/v1/get/list",
    #         headers={"token": tokens.access_token},
    #     )
    #     assert response.status_code == 200, response.json()
    #     assert response.json()["count"] == 10
    #     assert len(response.json()["items"]) == 10
    #
    # async def test_staff_list_sorting(self, token_data_factory):
    #     user = factories.UserFactory.create()
    #     tokens: schemas.TokenResponse = await token_data_factory(user)
    #
    #     factories.StaffFactory.create_batch(10)
    #     response = await self.client.get(
    #         "/api/staff/v1/get/list?sort=created_at",
    #         headers={"token": tokens.access_token},
    #     )
    #     assert response.status_code == 200, response.json()
    #     assert response.json()["count"] == 10
    #     assert len(response.json()["items"]) == 10

    async def test_staff_details(self):
        staff = factories.StaffFactory.create()
        response = await self.client.get(f"/api/staff/v1/get/{staff.id}")
        assert response.status_code == 200, response.json()

    async def test_staff_delete(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        staff = factories.StaffFactory.create()

        response = await self.client.delete(
            "/api/staff/v1/delete",
            json=dict(
                id=str(staff.id)
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()
