import enum

import pytest
from a8t_tools.security.permissions import PermissionsBase


class Roles(PermissionsBase):
    superuser = enum.auto()
    admin = enum.auto()
    terminal = enum.auto()
    operator = enum.auto()
    technician = enum.auto()
    security = enum.auto()
    shareholder = enum.auto()
    bot = enum.auto()


class Permissions(PermissionsBase):
    can_add_permissions = enum.auto()
    can_view_permissions = enum.auto()
    can_remove_permissions = enum.auto()

    can_create_admins = enum.auto()
    can_view_admins = enum.auto()
    can_edit_admins = enum.auto()
    can_remove_admins = enum.auto()
    can_block_admins = enum.auto()

    can_view_operators_worktime = enum.auto()
    can_view_sim_orders = enum.auto()
    can_view_documents = enum.auto()
    can_view_terminal_full_data = enum.auto()

    cannot_act_as_terminal_hardware = enum.auto()

    manage_software_update = enum.auto()


class TestPermissions:
    @pytest.mark.parametrize(
        "condition_lambda,existing_scopes,expected_result",
        [
            (
                lambda: ~Permissions.can_view_permissions,
                [Permissions.can_add_permissions],
                True,
            ),
            (
                lambda: ~Permissions.can_view_permissions,
                [Permissions.can_view_permissions],
                False,
            ),
        ],
    )
    def test_permissions(self, condition_lambda, existing_scopes, expected_result):
        node = condition_lambda()
        assert node.resolve(existing_scopes) is expected_result

    def test_invert_roles(self):
        node = ~Roles.admin

        assert node.resolve([Roles.terminal]) is True
        assert node.resolve([Roles.superuser]) is True
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Roles.superuser, Roles.terminal]) is True
        assert node.resolve([Roles.superuser, Roles.admin]) is False

    def test_or_permissions(self):
        node = Permissions.can_add_permissions | Permissions.can_view_permissions

        assert node.resolve([Permissions.can_add_permissions]) is True
        assert node.resolve([Permissions.can_view_permissions]) is True
        assert node.resolve([Permissions.can_remove_permissions]) is False
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is True
        )

    def test_or_roles(self):
        node = Roles.admin | Roles.terminal

        assert node.resolve([Roles.terminal]) is True
        assert node.resolve([Roles.superuser]) is False
        assert node.resolve([Roles.admin]) is True
        assert node.resolve([Roles.superuser, Roles.terminal]) is True
        assert node.resolve([Roles.superuser, Roles.admin]) is True
        assert node.resolve([Roles.admin, Roles.terminal]) is True

    def test_or_roles_permissions(self):
        node = (
            Roles.superuser
            | Permissions.can_add_permissions
            | Permissions.can_remove_permissions
        )

        assert node.resolve([Roles.terminal]) is False
        assert node.resolve([Roles.superuser]) is True
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Permissions.can_add_permissions]) is True
        assert node.resolve([Permissions.can_view_permissions]) is False
        assert node.resolve([Permissions.can_remove_permissions]) is True
        assert (
            node.resolve(
                [Roles.superuser, Roles.terminal, Permissions.can_add_permissions]
            )
            is True
        )
        assert node.resolve([Permissions.can_view_permissions, Roles.superuser]) is True
        assert node.resolve([Permissions.can_view_permissions, Roles.admin]) is False

    def test_and_permissions(self):
        node = Permissions.can_add_permissions & Permissions.can_view_permissions

        assert node.resolve([Permissions.can_add_permissions]) is False
        assert node.resolve([Permissions.can_view_permissions]) is False
        assert node.resolve([Permissions.can_remove_permissions]) is False
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is False
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is False
        )

    def test_and_roles(self):
        node = Roles.admin & Roles.terminal

        assert node.resolve([Roles.terminal]) is False
        assert node.resolve([Roles.superuser]) is False
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Roles.superuser, Roles.terminal]) is False
        assert node.resolve([Roles.superuser, Roles.admin]) is False
        assert node.resolve([Roles.admin, Roles.terminal]) is True

    def test_and_roles_permissions(self):
        node = Roles.admin & Roles.terminal & Permissions.can_view_permissions

        assert node.resolve([Roles.terminal]) is False
        assert node.resolve([Roles.superuser]) is False
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Roles.superuser, Roles.terminal]) is False
        assert node.resolve([Roles.superuser, Roles.admin]) is False
        assert node.resolve([Roles.admin, Roles.terminal]) is False
        assert (
            node.resolve(
                [Roles.admin, Roles.terminal, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Roles.admin, Roles.terminal, Permissions.can_remove_permissions]
            )
            is False
        )

    def test_or_and_permissions(self):
        node = (
            Permissions.can_add_permissions & Permissions.can_view_permissions
            | Permissions.can_remove_permissions
        )

        assert node.resolve([Permissions.can_add_permissions]) is False
        assert node.resolve([Permissions.can_view_permissions]) is False
        assert node.resolve([Permissions.can_remove_permissions]) is True
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is True
        )

    def test_or_and_roles(self):
        node = Roles.admin & Roles.terminal | Roles.superuser

        assert node.resolve([Roles.terminal]) is False
        assert node.resolve([Roles.superuser]) is True
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Roles.superuser, Roles.terminal]) is True
        assert node.resolve([Roles.superuser, Roles.admin]) is True
        assert node.resolve([Roles.admin, Roles.terminal]) is True

    def test_or_and_roles_permissions(self):
        node = (
            Permissions.can_add_permissions & Permissions.can_view_permissions
            | Roles.superuser
        )

        assert node.resolve([Roles.terminal]) is False
        assert node.resolve([Roles.superuser]) is True
        assert node.resolve([Roles.admin]) is False
        assert node.resolve([Roles.superuser, Roles.terminal]) is True
        assert node.resolve([Roles.superuser, Roles.admin]) is True
        assert node.resolve([Roles.admin, Roles.terminal]) is False
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is False
        )

    def test_or_and_custom_order(self):
        node = Permissions.can_add_permissions & (
            Permissions.can_view_permissions | Permissions.can_remove_permissions
        )

        assert node.resolve([Permissions.can_add_permissions]) is False
        assert node.resolve([Permissions.can_view_permissions]) is False
        assert node.resolve([Permissions.can_remove_permissions]) is False
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is False
        )

    def test_or_invert(self):
        node = Permissions.can_view_permissions | ~Permissions.can_add_permissions

        assert node.resolve([Permissions.can_add_permissions]) is False
        assert node.resolve([Permissions.can_view_permissions]) is True
        assert node.resolve([Permissions.can_remove_permissions]) is True
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_view_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is False
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is True
        )

    def test_and_invert_permissions(self):
        node = Permissions.can_view_permissions & ~Permissions.can_add_permissions

        assert node.resolve([Permissions.can_add_permissions]) is False
        assert node.resolve([Permissions.can_view_permissions]) is True
        assert node.resolve([Permissions.can_remove_permissions]) is False
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_add_permissions]
            )
            is False
        )
        assert (
            node.resolve(
                [Permissions.can_add_permissions, Permissions.can_remove_permissions]
            )
            is False
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is True
        )

    def test_and_invert_roles_permissions(self):
        node = (
            Permissions.can_view_permissions & Permissions.can_add_permissions
        ) | ~Roles.superuser

        assert node.resolve([Permissions.can_add_permissions, Roles.admin]) is True
        assert node.resolve([Permissions.can_view_permissions, Roles.admin]) is True
        assert (
            node.resolve([Permissions.can_view_permissions, Roles.superuser]) is False
        )
        assert (
            node.resolve([Permissions.can_remove_permissions, Roles.superuser]) is False
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_add_permissions]
            )
            is True
        )
        assert (
            node.resolve(
                [
                    Permissions.can_view_permissions,
                    Permissions.can_add_permissions,
                    Roles.superuser,
                ]
            )
            is True
        )
        assert (
            node.resolve(
                [
                    Permissions.can_view_permissions,
                    Permissions.can_add_permissions,
                    Roles.admin,
                ]
            )
            is True
        )
        assert (
            node.resolve(
                [
                    Permissions.can_add_permissions,
                    Permissions.can_remove_permissions,
                    Roles.superuser,
                ]
            )
            is False
        )
        assert (
            node.resolve(
                [Permissions.can_view_permissions, Permissions.can_remove_permissions]
            )
            is True
        )
