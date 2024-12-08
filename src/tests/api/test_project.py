import pytest

from app.domain.users.auth import schemas
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestProject:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_project_create(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        response = await self.client.post(
            "/api/projects/v1/create",
            json=dict(
                name="test_name",
                startDate="2024-12-08T12:41:20.135Z",
                endDate="2024-12-08T12:41:20.135Z",
                description="test_description",
                participants=5,
                lessons=10,
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()

    async def test_projects_list(self):
        factories.ProjectFactory.create_batch(10)
        response = await self.client.get("/api/projects/v1/get/list")
        assert response.status_code == 200, response.json()
        assert response.json()["count"] == 10
        assert len(response.json()["items"]) == 10

    async def test_projects_list_sorting(self):
        factories.ProjectFactory.create_batch(10)
        response = await self.client.get(
            "/api/projects/v1/get/list?sort=created_at"
        )
        assert response.status_code == 200, response.json()
        assert response.json()["count"] == 10
        assert len(response.json()["items"]) == 10

    async def test_project_details(self):
        project = factories.ProjectFactory.create()
        response = await self.client.get(f"/api/projects/v1/get/{project.id}")
        assert response.status_code == 200, response.json()

    async def test_project_delete(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        project = factories.ProjectFactory.create()

        response = await self.client.delete(
            "/api/projects/v1/delete",
            json=dict(
                id=str(project.id)
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()

    async def test_project_like(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        project = factories.ProjectFactory.create()

        response = await self.client.post(
            "/api/projects/v1/create/like",
            json=dict(
                project_id=str(project.id)
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()
