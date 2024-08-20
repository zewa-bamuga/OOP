from fastapi import APIRouter, status

import app.domain.storage.attachments.views
import app.domain.users.auth.views
import app.domain.users.management.views
import app.domain.users.registration.views
import app.domain.users.profile.views
import app.domain.users.staff.views
import app.domain.projects.views

from app.api import schemas

auth = APIRouter(prefix="/lol")
# auth.include_router(
#     app.domain.users.registration.views.router,
#     prefix="/v1",
#     tags=["Authentication"]
# )
auth.include_router(
    app.domain.users.auth.views.router,
    prefix="/v1",
    tags=["Authentication"]
)

staff = APIRouter(prefix="/staff")
staff.include_router(
    app.domain.users.staff.views.router,
    prefix="/v1",
    tags=["Staff"]
)

profile = APIRouter(prefix="/profile")
profile.include_router(
    app.domain.users.profile.views.router,
    prefix="/v1",
    tags=["Profile"],
)

projects = APIRouter(prefix="/projects")
projects.include_router(
    app.domain.projects.views.router,
    prefix="/v1",
    tags=["Projects"],
)

management = APIRouter(prefix="/management")
management.include_router(
    app.domain.users.management.views.router,
    prefix="/v1",
    tags=["users"],
)

storage_router = APIRouter(prefix="/storage")
# storage_router.include_router(
#     app.domain.storage.attachments.views.router,
#     prefix="/v1/attachments",
#     tags=["attachments"],
# )

router = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": schemas.AuthApiError},
        status.HTTP_403_FORBIDDEN: {"model": schemas.SimpleApiError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.SimpleApiError},
    }
)

router.include_router(auth)
router.include_router(projects)
router.include_router(staff)
router.include_router(profile)
router.include_router(management)
router.include_router(storage_router)
