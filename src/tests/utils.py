import asyncio
import functools
import inspect
from typing import Any

import pytest
from async_asgi_testclient import TestClient
from async_asgi_testclient.websocket import WebSocketSession
from factory import base


def decorate_db(fn):
    @functools.wraps(fn)
    async def wrapped(self, *args, **kwargs):
        async with self.db_transaction.use(force_rollback=True) as session:
            AsyncSQLAlchemyModelFactory.session = session
            ret = await fn(self, *args, **kwargs)
            AsyncSQLAlchemyModelFactory.session = None
            return ret

    return wrapped


def for_all_async_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:  # there's probably a better way to do this
            if asyncio.iscoroutinefunction(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def async_methods_in_db_transaction(fn=None):
    """
    This function wraps all async methods of the decorated class with async db test_db_transaction
    """

    @pytest.fixture(autouse=True)
    def __setup(self, db_transaction) -> None:
        self.db_transaction = db_transaction

    def decorated(cls):
        setattr(cls, "__setup", __setup)
        return for_all_async_methods(decorate_db)(cls)

    if fn is None:
        return decorated

    return decorated(fn)


class FixedWebSocketSession(WebSocketSession):
    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
        await self._app_task
        self._app_task = None


class TestClientSessionExpire(TestClient):
    async def open(self, *args, **kwargs):
        return await super().open(*args, **kwargs)

    def websocket_connect(self, path, headers=None, cookies=None):
        return FixedWebSocketSession(self, path, headers, cookies)


class AsyncSQLAlchemyModelFactory(base.Factory):
    """Base class for facotries."""

    session: Any

    class Meta:
        abstract = True
        exclude = ("session",)

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Create an instance of a model.
        :param args: factory args.
        :param kwargs: factory keyword-args.
        :return: created model.
        """
        instance = super().create(*args, **kwargs)
        asyncio.run(cls.session.flush())
        asyncio.run(cls.session.refresh(instance))
        return instance

    @classmethod
    def create_batch(cls, size: int, *args: Any, **kwargs: Any) -> list[Any]:
        """
        Create batch of instances.
        :param size: instances count.
        :param args: factory args.
        :param kwargs: factory keyword-args.
        :return: List of created models.
        """
        return [cls.create(*args, **kwargs) for _ in range(size)]

    @classmethod
    def _create(
        cls,
        model_class: type["AsyncSQLAlchemyModelFactory"],
        *args: Any,
        **kwargs: Any,
    ) -> "AsyncSQLAlchemyModelFactory":
        """
        Create a model.
        This function creates model with given arguments
        and stores it in current session.
        :param model_class: class for model generation.
        :param args: args for instance creation.
        :param **kwargs: kwargs for instance.
        :raises RuntimeError: if session was not provided.
        :return: created model.
        """
        if cls.session is None:
            raise RuntimeError("No session provided.")

        async def maker_coroutine() -> AsyncSQLAlchemyModelFactory:
            """
            Corutine that creates and saves model in DB.
            :return: created instance.
            """
            for key, value in kwargs.items():  # noqa: WPS110
                # This hack is used because when we
                # want to create an instance of async model
                # we might want to await the result of a function.
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            model = model_class(*args, **kwargs)
            cls.session.add(model)
            return model

        return asyncio.run(maker_coroutine())
