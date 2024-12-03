from typing import Any

import pytest

from app.domain.common import enums
from app.domain.users.auth import schemas
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestAuth:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_user_register(self, celery_app_mock):
        response = await self.client.post(
            "/api/authentication/v1/registration",
            json=dict(
                firstname="test_firstname",
                lastname="test_lastname",
                email="test@mail.ru",
                password="password",
            ),
        )
        assert response.status_code == 200, response.json()

    @pytest.mark.parametrize(
        ("real_password", "entered_password", "status_code"),
        [
            ("test", "test", 200),
            ("test", "ololo", 401),
            ("test", "test ", 401),
        ],
    )
    async def test_user_authenticate(
        self, container, real_password, entered_password, status_code
    ):
        phs = container.user.password_hash_service()
        user = factories.UserFactory.create(password_hash=phs.hash(real_password))

        response = await self.client.post(
            "/api/authentication/v1/authentication",
            json=dict(
                email=user.email,
                password=entered_password,
            ),
        )

        assert response.status_code == status_code, response.json()

        if status_code == 401:
            assert (
                enums.AuthErrorCodes.invalid_credentials
                == response.json()["payload"]["code"]
            )

    async def test_user_flow(self, celery_app_mock):
        response = await self.client.post(
            "/api/authentication/v1/registration",
            json=dict(
                firstname="test_firstname",
                lastname="test_lastname",
                email="test@mail.ru",
                password="password",
            ),
        )
        assert response.status_code == 200, response.json()

        response = await self.client.post(
            "/api/authentication/v1/authentication",
            json=dict(
                email="test@mail.ru",
                password="password",
            ),
        )
        response_data: dict[str, Any] = response.json()
        assert response.status_code == 200, response.json()
        assert response_data["accessToken"]

    async def test_refresh_tokens(self, container, token_data_factory):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        response = await self.client.post(
            "/api/authentication/v1/refresh",
            json=dict(
                refresh_token=tokens.refresh_token,
            ),
        )

        assert response.status_code == 200, response.json()

    async def test_refresh_token_invalid(self, container, token_data_factory):
        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        token_payload: schemas.TokenPayload = (
            await container.user.token_payload_query()(tokens.refresh_token)
        )
        await container.user.token_repository().delete_tokens(token_payload.sub)

        response = await self.client.post(
            "/api/authentication/v1/refresh",
            json=dict(
                refresh_token=tokens.refresh_token,
            ),
        )
        assert response.status_code == 401, response.json()
        assert response.json()["code"] == enums.ErrorCodes.auth_error
        assert response.json()["payload"]["code"] == enums.AuthErrorCodes.invalid_token
