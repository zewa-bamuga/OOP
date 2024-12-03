from tests import utils


@utils.async_methods_in_db_transaction
class TestTyper:
    async def test_create_superuser(
        self, container_singletone, db_transaction, celery_app_mock
    ):
        from app import typer

        typer.create_superuser("test", "test", "test@mail.ru", "test")

    async def test_create_superuser_multiple_does_not_throw_error(
        self, container_singletone, db_transaction, celery_app_mock
    ):
        from app import typer

        typer.create_superuser("test", "test", "test@mail.ru", "test")
        typer.create_superuser("test", "test", "test@mail.ru", "test")
