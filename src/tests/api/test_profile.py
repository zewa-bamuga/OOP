from typing import Any

import pytest

from tests import utils, factories

from app.domain.users.auth import schemas


@utils.async_methods_in_db_transaction
class TestAuth:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_user_profile(self, token_data_factory, celery_app_mock):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        response = await self.client.get(
            "/api/profile/v1/me",
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()
