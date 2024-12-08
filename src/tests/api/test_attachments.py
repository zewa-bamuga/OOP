from unittest import mock

import boto3
import pytest
from unittest.mock import patch
from moto import mock_aws

from app.domain.users.auth import schemas
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestAttachments:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    @patch("boto3.client")
    async def test_attachment_create(self, mock_boto_client, token_data_factory, fs, frozen_time, local_storage_mock):
        mock_s3_client = mock_boto_client.return_value
        mock_s3_client.upload_file.return_value = None

        expected_uri = "http://test_uri"
        expected_name = "testfile"
        file = fs.create_file(f"/{expected_name}", contents="test")
        expected_time = frozen_time.time_to_freeze
        local_storage_mock.upload_file.return_value = expected_uri

        user = factories.UserFactory.create()
        tokens: schemas.TokenResponse = await token_data_factory(user)

        response = await self.client.post(
            "/api/storage/v1/attachments/create",
            files=dict(
                attachment=(
                    file.name,
                    open(file.path, "rb"),
                    "text/plain",
                )
            ),
            headers={"token": tokens.access_token},
        )
        assert response.status_code == 200, response.json()

    async def test_attachments_list(self):
        factories.AttachmentFactory.create_batch(10)
        response = await self.client.get("/api/storage/v1/attachments/get")
        assert response.status_code == 200, response.json()
        assert response.json()["count"] == 10
        assert len(response.json()["items"]) == 10

    async def test_attachments_list_sorting(self):
        factories.AttachmentFactory.create_batch(10)
        response = await self.client.get(
            "/api/storage/v1/attachments/get?sort=created_at"
        )
        assert response.status_code == 200, response.json()
        assert response.json()["count"] == 10
        assert len(response.json()["items"]) == 10

    async def test_attachments_list_sorting_unknown_field(self):
        response = await self.client.get(
            "/api/storage/v1/attachments/get?sort=some_nonexistent_field"
        )
        assert response.status_code == 422, response.json()

    async def test_attachment_details(self):
        attachment = factories.AttachmentFactory.create()
        response = await self.client.get(f"/api/storage/v1/attachments/{attachment.id}")
        assert response.status_code == 200, response.json()
