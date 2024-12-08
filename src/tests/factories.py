import factory

from app.domain.common import enums, models
from tests import utils


class AttachmentFactory(utils.AsyncSQLAlchemyModelFactory):
    name = factory.Faker("name")
    path = factory.Faker("name")
    uri = factory.Faker("uri")

    class Meta:
        model = models.Attachment


class UserFactory(utils.AsyncSQLAlchemyModelFactory):
    firstname = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    email = factory.Faker("email")
    description = factory.Faker("text")
    password_hash = factory.Faker("password")
    status = factory.Faker("random_element", elements=enums.UserStatuses)
    avatar_attachment = factory.SubFactory(AttachmentFactory)
    permissions = {}

    class Meta:
        model = models.User


class StaffFactory(utils.AsyncSQLAlchemyModelFactory):
    firstname = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    qualification = factory.Faker("text")
    post = factory.Faker("text")
    email = factory.Faker("email")
    description = factory.Faker("text")
    link_to_vk = factory.Faker("text")
    password_hash = factory.Faker("password")
    status = factory.Faker("random_element", elements=enums.UserStatuses)
    avatar_attachment = factory.SubFactory(AttachmentFactory)
    permissions = {}

    class Meta:
        model = models.Staff


class ProjectFactory(utils.AsyncSQLAlchemyModelFactory):
    name = factory.Faker("name")
    start_date = factory.Faker("date_this_year")
    end_date = factory.Faker("date_this_year")
    description = factory.Faker("text")
    participants = factory.Faker("random_int", min=1, max=100)
    lessons = factory.Faker("random_int", min=1, max=100)
    likes = factory.Faker("random_int", min=0, max=100)
    avatar_attachment = factory.SubFactory(AttachmentFactory)

    class Meta:
        model = models.Project


class ProjectLikeFactory(utils.AsyncSQLAlchemyModelFactory):
    user_id = factory.Faker("user_id")
    project_id = factory.Faker("project_id")

    class Meta:
        model = models.ProjectLike


class EmailVerificationCodeFactory(utils.AsyncSQLAlchemyModelFactory):
    email = factory.Faker("email")
    code = factory.Faker("code")

    class Meta:
        model = models.EmailCode


class PasswordResetCodeFactory(utils.AsyncSQLAlchemyModelFactory):
    user_id = factory.Faker("user_id")
    code = factory.Faker("code")

    class Meta:
        model = models.PasswordResetCode
