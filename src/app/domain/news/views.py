from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, UploadFile, Header
from fastapi.params import Form

from app.api import deps
from app.containers import Container
from app.domain.news.commands import NewsCreateCommand
from app.domain.news.schemas import NewsCreate
from app.domain.projects.queries import ProjectManagementListQuery, ProjectRetrieveQuery
from app.domain.projects.schemas import Project, ProjectCreate, LikeTheProject, Like, AddEmployees
from app.domain.projects.commands import ProjectCreateCommand, LikeTheProjectCommand, UnlikeTheProjectCommand, \
    AddEmployeesCommand
from app.domain.projects import schemas
from app.domain.storage.attachments import schemas as AttachmentSchema
from app.domain.storage.attachments.commands import AttachmentCreateCommand, ProjectAttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from a8t_tools.db import pagination, sorting

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post(
    "/create",
    response_model=None
)
@wiring.inject
async def create_news(
        payload: NewsCreate,
        token: str = Header(...),
        command: NewsCreateCommand = Depends(wiring.Provide[Container.news.create_command]),
):
    async with user_token(token):
        news = await command(payload)
        return news
