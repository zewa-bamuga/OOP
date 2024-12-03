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
