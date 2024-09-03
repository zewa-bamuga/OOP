import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from loguru import logger

import app.domain
from app.containers import Container
from app.domain.users.core.schemas import UserCreate, StaffCreate
from app.domain.users.permissions.schemas import BasePermissions
from a8t_tools.db.exceptions import DatabaseError


def async_to_sync(fn: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coro = fn(*args, **kwargs)
        return asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


def create_container() -> Container:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()
    return container


container = create_container()
typer_app = typer.Typer()


@typer_app.command()
@async_to_sync
async def noop() -> None:
    pass


@typer_app.command()
@async_to_sync
async def create_superuser(
        firstname: str = typer.Argument(...),
        lastname: str = typer.Argument(...),
        email: str = typer.Argument(...),
        password: str = typer.Argument(...),
) -> None:
    password_hash = await container.user.password_hash_service().hash(password)
    command = container.user.create_command()
    try:
        await command(
            UserCreate(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password_hash=password_hash,
                permissions={BasePermissions.superuser},
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Superuser creation error: {err}")


@typer_app.command()
@async_to_sync
async def create_staff(
        firstname: str = typer.Argument(...),
        lastname: str = typer.Argument(...),
        qualification: str = typer.Argument(...),
        post: str = typer.Argument(...),
        email: str = typer.Argument(...),
        description: str = typer.Argument(...),
        link_to_vk: str = typer.Argument(...),
) -> None:
    generate_password = container.user.generate_password()
    password_hash = await container.user.password_hash_service().hash(generate_password)
    command = container.user.create_command()
    try:
        await command(
            StaffCreate(
                firstname=firstname,
                lastname=lastname,
                qualification=qualification,
                post=post,
                email=email,
                description=description,
                link_to_vk=link_to_vk,
                password_hash=password_hash,
                permissions={BasePermissions.employee},
            ),
        )
        await container.user.first_registration(email, generate_password)

    except DatabaseError as err:
        logger.warning(f"Employee creation error: {err}")