import re
import uuid
from datetime import datetime
from uuid import UUID

from a8t_tools.storage.facade import FileStorage

from app.domain.common.exceptions import NotFoundError
from app.domain.storage.attachments.repositories import AttachmentRepository
from app.domain.storage.attachments.schemas import (
    AttachmentCreate,
    AttachmentCreateFull,
)
from app.domain.users.core.repositories import StaffRepository
from app.domain.users.staff import schemas
from app.domain.users.staff.queries import StaffRetrieveQuery
from app.domain.users.staff.schemas import StaffCreate, StaffPartialUpdate


class StaffCreateCommand:
    def __init__(
        self,
        staff_repository: StaffRepository,
    ) -> None:
        self.staff_repository = staff_repository

    async def __call__(self, payload: StaffCreate) -> None:
        staff_create_data = schemas.StaffCreate(
            firstname=payload.firstname,
            lastname=payload.lastname,
            email=payload.email,
            qualification=payload.qualification,
            post=payload.post,
            description=payload.description,
            link_to_vk=payload.link_to_vk,
        )

        staff_id_container = await self.staff_repository.create_employee(
            staff_create_data
        )

        staff = await self.staff_repository.get_employee_by_filter_or_none(
            schemas.StaffWhere(id=staff_id_container.id)
        )

        assert staff

        return schemas.StaffDetails.model_validate(staff)


class StaffDeleteCommand:
    def __init__(self, staff_repository: StaffRepository) -> None:
        self.staff_repository = staff_repository

    async def __call__(self, payload: schemas.StaffDelete) -> None:
        return await self.staff_repository.delete_staff(payload.id)


class StaffPartialUpdateCommand:
    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    async def __call__(
        self, staff_id: UUID, payload: schemas.StaffPartialUpdate
    ) -> schemas.StaffDetailsFull:
        try:
            await self.staff_repository.partial_update_staff(staff_id, payload)
            staff = await self.staff_repository.get_staff_by_filter_or_none(
                schemas.StaffWhere(id=staff_id)
            )

            if not staff:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении сотрудника:", e)
            raise

        return schemas.StaffDetailsFull.model_validate(staff)


class StaffAvatarCreateCommand:
    def __init__(
        self,
        repository: AttachmentRepository,
        file_storage: FileStorage,
        staff_retrieve_by_id_query: StaffRetrieveQuery,
        staff_partial_update_command: StaffPartialUpdateCommand,
        bucket: str,
        max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.staff_retrieve_by_id_query = staff_retrieve_by_id_query
        self.staff_partial_update_command = staff_partial_update_command
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(
        self, staff_id: UUID, attachment_payload: AttachmentCreate
    ) -> schemas.Attachment:
        current_staff = await self.staff_retrieve_by_id_query(staff_id)

        name = attachment_payload.name or self._get_random_name()
        path = self._generate_path(name)

        uri = await self.file_storage.upload_file(
            self.bucket, path, attachment_payload.file
        )

        if "/department-of-educational-programs-bucket/" in uri:
            uri = uri.replace("/department-of-educational-programs-bucket/", "/")

        id_container = await self.repository.create_attachment(
            AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )

        attachment = await self.repository.get_attachment_or_none(id_container.id)
        attachment_id = attachment.id

        update_payload = StaffPartialUpdate(avatar_attachment_id=attachment_id)

        await self.staff_partial_update_command(current_staff.id, update_payload)

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
