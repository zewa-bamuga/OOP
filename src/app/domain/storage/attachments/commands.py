from a8t_tools.storage.facade import FileStorage
from datetime import datetime
import uuid
import re
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import IO

from app.domain.clips.commands import ClipPartialUpdateCommand
from app.domain.clips.queries import ClipRetrieveQuery
from app.domain.clips.schemas import ClipPartialUpdate
from app.domain.news.commands import NewsPartialUpdateCommand
from app.domain.news.queries import NewsRetrieveQuery
from app.domain.news.schemas import NewsPartialUpdate
from app.domain.projects.commands import ProjectPartialUpdateCommand
from app.domain.projects.queries import ProjectRetrieveQuery
from app.domain.projects.schemas import Like, ProjectPartialUpdate
from app.domain.storage.attachments import schemas
from app.domain.users.core import schemas as lol
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.users.core.commands import UserPartialUpdateCommand
from app.domain.users.profile.queries import UserProfileMeQuery


class AttachmentCreateCommand:
    def __init__(
            self,
            repository: AttachmentRepository,
            file_storage: FileStorage,
            current_user_query: UserProfileMeQuery,
            user_partial_update_command: UserPartialUpdateCommand,
            bucket: str,
            max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.current_user_query = current_user_query
        self.user_partial_update_command = user_partial_update_command
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(self, payload: schemas.AttachmentCreate) -> schemas.Attachment:
        current_user = await self.current_user_query()

        name = payload.name or self._get_random_name()
        path = self._generate_path(name)

        # Загружаем файл и получаем uri
        uri = await self.file_storage.upload_file(self.bucket, path, payload.file)

        # Если uri содержит лишний сегмент, исправляем его
        if '/department-of-educational-programs-bucket/' in uri:
            uri = uri.replace('/department-of-educational-programs-bucket/', '/')

        id_container = await self.repository.create_attachment(
            schemas.AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )

        attachment = await self.repository.get_attachment_or_none(id_container.id)
        attachment_id = attachment.id

        update_payload = lol.UserPartialUpdate(avatar_attachment_id=attachment_id)

        await self.user_partial_update_command(current_user.id, update_payload)

        assert attachment
        return attachment

    def _generate_path(self, name: str) -> str:
        now = datetime.now()
        folder = now.strftime("%Y/%m/%d")
        timestamp = now.strftime("%s")
        stripped_slugified_name = self._slugify(name)[: self.max_name_len]
        return f"/{folder}/{timestamp}.{stripped_slugified_name}"

    @classmethod
    def _get_random_name(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _slugify(cls, s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s\.-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s


class ProjectAttachmentCreateCommand:
    def __init__(
            self,
            repository: AttachmentRepository,
            file_storage: FileStorage,
            current_project_query: ProjectRetrieveQuery,
            project_partial_update_command: ProjectPartialUpdateCommand,
            bucket: str,
            max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.current_project_query = current_project_query
        self.project_partial_update_command = project_partial_update_command
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(self, like_payload: Like, attachment_payload: schemas.AttachmentCreate) -> schemas.Attachment:
        current_project = await self.current_project_query(like_payload.project_id)

        name = attachment_payload.name or self._get_random_name()
        path = self._generate_path(name)

        # Загружаем файл и получаем uri
        uri = await self.file_storage.upload_file(self.bucket, path, attachment_payload.file)

        # Если uri содержит лишний сегмент, исправляем его
        if '/department-of-educational-programs-bucket/' in uri:
            uri = uri.replace('/department-of-educational-programs-bucket/', '/')

        id_container = await self.repository.create_attachment(
            schemas.AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )

        attachment = await self.repository.get_attachment_or_none(id_container.id)
        attachment_id = attachment.id

        update_payload = ProjectPartialUpdate(avatar_attachment_id=attachment_id)

        await self.project_partial_update_command(current_project.id, update_payload)

        assert attachment
        return attachment

    def _generate_path(self, name: str) -> str:
        now = datetime.now()
        folder = now.strftime("%Y/%m/%d")
        timestamp = now.strftime("%s")
        stripped_slugified_name = self._slugify(name)[: self.max_name_len]
        return f"/{folder}/{timestamp}.{stripped_slugified_name}"

    @classmethod
    def _get_random_name(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _slugify(cls, s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s\.-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s


class NewsAttachmentCreateCommand:
    def __init__(
            self,
            repository: AttachmentRepository,
            file_storage: FileStorage,
            current_news_query: NewsRetrieveQuery,
            news_partial_update_command: NewsPartialUpdateCommand,
            bucket: str,
            max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.current_news_query = current_news_query
        self.news_partial_update_command = news_partial_update_command
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(self, like_payload: Like, attachment_payload: schemas.AttachmentCreate) -> schemas.Attachment:
        current_news = await self.current_news_query(like_payload.news_id)

        name = attachment_payload.name or self._get_random_name()
        path = self._generate_path(name)

        # Загружаем файл и получаем uri
        uri = await self.file_storage.upload_file(self.bucket, path, attachment_payload.file)

        # Если uri содержит лишний сегмент, исправляем его
        if '/department-of-educational-programs-bucket/' in uri:
            uri = uri.replace('/department-of-educational-programs-bucket/', '/')

        id_container = await self.repository.create_attachment(
            schemas.AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )

        attachment = await self.repository.get_attachment_or_none(id_container.id)
        attachment_id = attachment.id

        update_payload = NewsPartialUpdate(avatar_attachment_id=attachment_id)

        await self.news_partial_update_command(current_news.id, update_payload)

        assert attachment
        return attachment

    def _generate_path(self, name: str) -> str:
        now = datetime.now()
        folder = now.strftime("%Y/%m/%d")
        timestamp = now.strftime("%s")
        stripped_slugified_name = self._slugify(name)[: self.max_name_len]
        return f"/{folder}/{timestamp}.{stripped_slugified_name}"

    @classmethod
    def _get_random_name(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _slugify(cls, s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s\.-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s


class ClipAttachmentCreateCommand:
    def __init__(
            self,
            repository: AttachmentRepository,
            file_storage: FileStorage,
            current_clip_query: ClipRetrieveQuery,
            clip_partial_update_command: ClipPartialUpdateCommand,
            bucket: str,
            max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.current_clip_query = current_clip_query
        self.clip_partial_update_command = clip_partial_update_command
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(self, like_payload: Like, attachment_payload: schemas.AttachmentCreate) -> schemas.Attachment:
        current_clip = await self.current_clip_query(like_payload.clip_id)

        name = attachment_payload.name or self._get_random_name()
        path = self._generate_path(name)

        # Загружаем файл и получаем uri
        uri = await self.file_storage.upload_file(self.bucket, path, attachment_payload.file)

        # Если uri содержит лишний сегмент, исправляем его
        if '/department-of-educational-programs-bucket/' in uri:
            uri = uri.replace('/department-of-educational-programs-bucket/', '/')

        id_container = await self.repository.create_attachment(
            schemas.AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )

        attachment = await self.repository.get_attachment_or_none(id_container.id)
        attachment_id = attachment.id

        update_payload = ClipPartialUpdate(clip_attachment_id=attachment_id)

        await self.clip_partial_update_command(current_clip.id, update_payload)

        assert attachment
        return attachment

    def _generate_path(self, name: str) -> str:
        now = datetime.now()
        folder = now.strftime("%Y/%m/%d")
        timestamp = now.strftime("%s")
        stripped_slugified_name = self._slugify(name)[: self.max_name_len]
        return f"/{folder}/{timestamp}.{stripped_slugified_name}"

    @classmethod
    def _get_random_name(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _slugify(cls, s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s\.-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s


class AttachmentDataRetrieveCommand:
    def __init__(
            self,
            file_storage: FileStorage,
            bucket: str,
    ):
        self.file_storage = file_storage
        self.bucket = bucket

    @asynccontextmanager
    async def __call__(self, attachment: schemas.Attachment) -> AsyncIterator[IO[bytes]]:
        async with self.file_storage.receive_file(self.bucket, attachment.path) as file:
            yield file
