from app.containers import Container
from app.domain.common import enums
from app.domain.users.core import schemas
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestUsers:
    async def test_list(self, container: Container):
        factories.UserFactory.create_batch(10)
        results = await container.user.user_list_query()(
            schemas.UserListRequestSchema()
        )
        assert len(results.items) == 13
        assert isinstance(results.items[0], schemas.User)

    async def test_retrieve(self, container: Container):
        user = factories.UserFactory.create()
        results = await container.user.retrieve_query()(user.id)
        assert isinstance(results, schemas.UserInternal)

    async def test_user_create(self, container: Container, celery_app_mock):
        attachment = factories.AttachmentFactory.create()
        user = await container.user.create_command()(
            schemas.UserCreate(
                firstname="test_firstname",
                lastname="test_lastname",
                email="test@mail.ru",
                avatar_attachment_id=attachment.id,
                password_hash="password_hash",
            )
        )

        celery_app_mock.send_task.assert_called_once_with(
            enums.TaskNames.activate_user,
            args=(),
            kwargs=dict(user_id_container_dict=dict(id=str(user.id))),
            queue=enums.TaskQueues.main_queue,
        )
