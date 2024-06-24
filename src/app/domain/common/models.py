import datetime
import secrets
import uuid

import sqlalchemy as sa
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Attachment(Base):
    __tablename__ = "attachment"

    name: orm.Mapped[str]
    path: orm.Mapped[str]
    uri: orm.Mapped[str | None]


class User(Base):
    __tablename__ = "user"

    username = Column(String, unique=True)
    email = Column(String, unique=True)
    status = Column(String)
    password_hash = Column(String)
    avatar_attachment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    permissions: orm.Mapped[set[str] | None] = orm.mapped_column(ARRAY(sa.String))

    avatar_attachment = relationship(
        "Attachment",
        backref="user_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )
    tokens = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=False)
    refresh_token_id = Column(UUID(as_uuid=True))

    user = relationship("User", back_populates="tokens")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    code = Column(String, nullable=False)

    user = relationship("User")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)
