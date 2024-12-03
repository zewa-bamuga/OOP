import re
import uuid
from datetime import datetime

from a8t_tools.storage.facade import FileStorage

from app.domain.storage.attachments import schemas
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.core import schemas as lol
from app.domain.users.core.commands import UserPartialUpdateCommand
from app.domain.users.core.schemas import UserPartialUpdateFull
from app.domain.users.profile.queries import UserProfileMeQuery
from app.domain.users.profile.schemas import UserProfilePartialUpdate


class UserProfilePartialUpdateCommand:
    def __init__(
        self,
        current_user_query: CurrentUserQuery,
        user_partial_update_command: UserPartialUpdateCommand,
    ) -> None:
        self.current_user_query = current_user_query
        self.user_partial_update_command = user_partial_update_command

    async def __call__(self, payload: UserProfilePartialUpdate) -> None:
        current_user = await self.current_user_query()
        await self.user_partial_update_command(
            current_user.id,
            UserPartialUpdateFull(**payload.model_dump(exclude_unset=True)),
        )


class UserAvatarCreateCommand:
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
        if "/department-of-educational-programs-bucket/" in uri:
            uri = uri.replace("/department-of-educational-programs-bucket/", "/")

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
