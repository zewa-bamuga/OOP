import os

import pytest
from a8t_tools.storage.local_storage import LocalStorageBackend


@pytest.fixture()
def base_path():
    return "/media"


@pytest.fixture()
def base_uri():
    return "http://localhost"


class TestLocalStorage:
    @pytest.fixture(autouse=True)
    def setup(self, base_path: str, base_uri: str):
        self.service = LocalStorageBackend(base_path=base_path, base_uri=base_uri)

    @pytest.mark.parametrize(
        "bucket, expected_uri",
        [
            ("media", "http://localhost/media/some_path/testfile"),
            ("", "http://localhost/some_path/testfile"),
        ],
    )
    async def test_upload_file(
        self, fs, base_path: str, base_uri: str, bucket: str, expected_uri: str
    ):
        name = "some_path/testfile"
        expected_path = f"{base_path}/{bucket}/{name}"
        file = fs.create_file(f"/{expected_path}", contents="test")

        uri = await self.service.upload_file(bucket, name, open(file.path, "rb"))
        assert os.path.exists(expected_path)
        assert uri == expected_uri
