from tests import utils


@utils.async_methods_in_db_transaction
class TestCelery:
    async def test_celery_import(self, container_singletone):
        from app import celery

        assert celery.celery_app
