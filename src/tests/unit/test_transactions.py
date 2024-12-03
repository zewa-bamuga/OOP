from unittest.mock import Mock

import pytest
from a8t_tools.db.transactions import AsyncDbTransaction, _on_commit_registry

from app.config import Settings

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
def transaction():
    settings = Settings()
    return AsyncDbTransaction(settings.db.dsn)


class TestTransactionsOnCommit:
    @pytest.fixture(autouse=True)
    def setup(self, client, transaction):
        self.transaction = transaction

    async def test_on_commit_simple(self):
        def test_function():
            return None

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            lambda_func_2 = lambda: test_function()  # noqa: E731
            mock_1 = Mock(lambda_func_1)
            mock_2 = Mock(lambda_func_2)
            self.transaction.on_commit(mock_1)
            self.transaction.on_commit(mock_2)

            assert mock_1 in _on_commit_registry.get([])
            assert mock_2 in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 2
            mock_1.assert_not_called()
            mock_2.assert_not_called()

        assert mock_1 not in _on_commit_registry.get([])
        assert mock_2 not in _on_commit_registry.get([])
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    async def test_on_commit_simple_awaitable(self, capsys):
        async def test_function():
            print("ololo")

        async with self.transaction.use():
            lambda_func_1 = test_function()  # noqa: E731
            self.transaction.on_commit(lambda_func_1)

        out, _ = capsys.readouterr()
        assert out == "ololo\n"

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    async def test_on_commit_simple_lambda_awaitable_works(self, capsys):
        async def test_function():
            print("ololo")

        async with self.transaction.use():
            lambda_func_2 = lambda: test_function()  # noqa: E731
            self.transaction.on_commit(lambda_func_2)

        out, _ = capsys.readouterr()
        assert out == "ololo\n"

    async def test_on_commit_multiple_sessions(self):
        def test_function():
            raise Exception()

        async with self.transaction.use():
            lambda_func = lambda: test_function()  # noqa: E731
            mock = Mock(lambda_func)
            self.transaction.on_commit(mock)
            assert len(_on_commit_registry.get([])) == 1

        mock.assert_called_once()

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            mock_1 = Mock(lambda_func_1)
            self.transaction.on_commit(mock_1)

            assert mock_1 in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 1
            mock_1.assert_not_called()

        async with self.transaction.use():
            assert len(_on_commit_registry.get([])) == 0

        assert mock_1 not in _on_commit_registry.get([])
        mock.assert_called_once()
        mock_1.assert_called_once()

    async def test_on_commit_with_error_in_callback(self):
        def test_function():
            return None

        def test_function_raise_error():
            raise Exception()

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            lambda_func_2 = lambda: test_function_raise_error()  # noqa: E731
            mock_1 = Mock(lambda_func_1)
            mock_2 = Mock(lambda_func_2)
            self.transaction.on_commit(mock_1)
            self.transaction.on_commit(mock_2)

            assert mock_1 in _on_commit_registry.get([])
            assert mock_2 in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 2
            mock_1.assert_not_called()
            mock_2.assert_not_called()

        assert mock_1 not in _on_commit_registry.get([])
        assert mock_2 not in _on_commit_registry.get([])
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    async def test_on_commit_transaction_error(self):
        def test_function():
            raise Exception()

        with pytest.raises(ValueError):
            async with self.transaction.use():
                lambda_func = lambda: test_function()  # noqa: E731
                mock = Mock(lambda_func)
                self.transaction.on_commit(mock)

                mock.assert_not_called()
                raise ValueError

        mock.assert_not_called()

        async with self.transaction.use():
            assert len(_on_commit_registry.get([])) == 0
            mock.assert_not_called()

        mock.assert_not_called()

    async def test_on_commit_force_rollback(self):
        def test_function():
            raise Exception()

        async with self.transaction.use(force_rollback=True):
            lambda_func = lambda: test_function()  # noqa: E731
            mock = Mock(lambda_func)
            self.transaction.on_commit(mock)

            mock.assert_not_called()

        mock.assert_not_called()

        async with self.transaction.use():
            assert len(_on_commit_registry.get([])) == 0
            mock.assert_not_called()

        mock.assert_not_called()

    async def test_on_commit_nested_with_force_rollback(self):
        def test_function():
            return None

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            lambda_func_2 = lambda: test_function()  # noqa: E731

            mock_1 = Mock(lambda_func_1)
            mock_2 = Mock(lambda_func_2)

            self.transaction.on_commit(mock_1)

            async with self.transaction.use(force_rollback=True):
                self.transaction.on_commit(mock_2)
                assert mock_1 not in _on_commit_registry.get([])
                assert mock_2 in _on_commit_registry.get([])
                assert len(_on_commit_registry.get([])) == 1
                mock_1.assert_not_called()
                mock_2.assert_not_called()

            assert mock_1 in _on_commit_registry.get([])
            assert mock_2 not in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 1
            mock_1.assert_not_called()
            mock_2.assert_not_called()

        assert mock_1 not in _on_commit_registry.get([])
        assert mock_2 not in _on_commit_registry.get([])
        mock_1.assert_called_once()
        mock_2.assert_not_called()

    async def test_on_commit_nested_with_exception(self):
        def test_function():
            return None

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            lambda_func_2 = lambda: test_function()  # noqa: E731

            mock_1 = Mock(lambda_func_1)
            mock_2 = Mock(lambda_func_2)

            self.transaction.on_commit(mock_1)

            with pytest.raises(ValueError):
                async with self.transaction.use():
                    self.transaction.on_commit(mock_2)
                    assert mock_1 not in _on_commit_registry.get([])
                    assert mock_2 in _on_commit_registry.get([])
                    assert len(_on_commit_registry.get([])) == 1
                    mock_1.assert_not_called()
                    mock_2.assert_not_called()
                    raise ValueError

            assert mock_1 in _on_commit_registry.get([])
            assert mock_2 not in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 1
            mock_1.assert_not_called()
            mock_2.assert_not_called()

        assert mock_1 not in _on_commit_registry.get([])
        assert mock_2 not in _on_commit_registry.get([])
        mock_1.assert_called_once()
        mock_2.assert_not_called()

    async def test_on_commit_nested(self):
        def test_function():
            return None

        async with self.transaction.use():
            lambda_func_1 = lambda: test_function()  # noqa: E731
            lambda_func_2 = lambda: test_function()  # noqa: E731

            mock_1 = Mock(lambda_func_1)
            mock_2 = Mock(lambda_func_2)

            self.transaction.on_commit(mock_1)

            async with self.transaction.use():
                self.transaction.on_commit(mock_2)
                assert mock_1 not in _on_commit_registry.get([])
                assert mock_2 in _on_commit_registry.get([])
                assert len(_on_commit_registry.get([])) == 1
                mock_1.assert_not_called()
                mock_2.assert_not_called()

            assert mock_1 in _on_commit_registry.get([])
            assert mock_2 in _on_commit_registry.get([])
            assert len(_on_commit_registry.get([])) == 2
            mock_1.assert_not_called()
            mock_2.assert_not_called()

        assert mock_1 not in _on_commit_registry.get([])
        assert mock_2 not in _on_commit_registry.get([])
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    async def test_on_commit_nested_multilevel(self):
        mock = Mock(lambda: None)

        async with self.transaction.use():
            self.transaction.on_commit(mock)  # 1

            async with self.transaction.use(force_rollback=True):
                self.transaction.on_commit(mock)  # noop

            async with self.transaction.use(force_rollback=False):
                self.transaction.on_commit(mock)  # 2

            with pytest.raises(ValueError):
                async with self.transaction.use():
                    self.transaction.on_commit(mock)  # noop
                    raise ValueError

            async with self.transaction.use(force_rollback=True):
                async with self.transaction.use():
                    async with self.transaction.use():
                        self.transaction.on_commit(mock)  # noop

            with pytest.raises(ValueError):
                async with self.transaction.use():
                    async with self.transaction.use():
                        async with self.transaction.use():
                            self.transaction.on_commit(mock)  # noop
                        raise ValueError

            async with self.transaction.use():
                async with self.transaction.use():
                    async with self.transaction.use(force_rollback=True):
                        self.transaction.on_commit(mock)  # noop
                    with pytest.raises(ValueError):
                        async with self.transaction.use(force_rollback=False):
                            self.transaction.on_commit(mock)  # noop
                            raise ValueError
                    async with self.transaction.use():
                        self.transaction.on_commit(mock)  # 3
                    self.transaction.on_commit(mock)  # 4

        assert mock.call_count == 4

    async def test_on_commit_multiple(self):
        mock = Mock(lambda: None)

        async with self.transaction.use(force_rollback=True):
            self.transaction.on_commit(mock)  # noop
        assert mock.call_count == 0

        async with self.transaction.use(force_rollback=False):
            self.transaction.on_commit(mock)  # 1
        assert mock.call_count == 1

        with pytest.raises(ValueError):
            async with self.transaction.use():
                self.transaction.on_commit(mock)  # noop
                raise ValueError
        assert mock.call_count == 1

        async with self.transaction.use(force_rollback=True):
            async with self.transaction.use():
                async with self.transaction.use():
                    self.transaction.on_commit(mock)  # noop
        assert mock.call_count == 1

        with pytest.raises(ValueError):
            async with self.transaction.use():
                async with self.transaction.use():
                    async with self.transaction.use():
                        self.transaction.on_commit(mock)  # noop
                    raise ValueError
        assert mock.call_count == 1

        async with self.transaction.use():
            async with self.transaction.use():
                async with self.transaction.use(force_rollback=True):
                    self.transaction.on_commit(mock)  # noop
                with pytest.raises(ValueError):
                    async with self.transaction.use(force_rollback=False):
                        self.transaction.on_commit(mock)  # noop
                        raise ValueError
                async with self.transaction.use():
                    self.transaction.on_commit(mock)  # 2
                self.transaction.on_commit(mock)  # 3
        assert mock.call_count == 3
