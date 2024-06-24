import enum

from a8t_tools.security.permissions import PermissionsBase


class BasePermissions(PermissionsBase):
    superuser = enum.auto()
    authenticated = enum.auto()

