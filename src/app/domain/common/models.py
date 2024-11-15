import datetime
import secrets
import uuid

import sqlalchemy as sa
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import random


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

    firstname = Column(String, unique=False, nullable=True)
    lastname = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=True)
    description = Column(String, unique=False, nullable=True)
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
    password_reset_code = relationship("PasswordResetCode", back_populates="user")


class Staff(Base):
    __tablename__ = "staff"

    firstname = Column(String, unique=False, nullable=True)
    lastname = Column(String, unique=False, nullable=True)
    qualification = Column(String, unique=False, nullable=True)
    post = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=True)
    description = Column(String, unique=False, nullable=True)
    link_to_vk = Column(String, unique=False, nullable=True)
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
        backref="staff_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )
    tokens = relationship("Token", back_populates="staff")
    password_reset_code = relationship("PasswordResetCode", back_populates="staff")

    projects = relationship("ProjectStaff", back_populates="staff")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey(Staff.id, ondelete="CASCADE"), index=True, nullable=True)
    refresh_token_id = Column(UUID(as_uuid=True))

    user = relationship("User", back_populates="tokens")
    staff = relationship("Staff", back_populates="tokens")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey(Staff.id, ondelete="CASCADE"), index=True, nullable=True)
    code = Column(String, nullable=False)

    user_id_user_fk = ForeignKey('user.id')
    user_id_staff_fk = ForeignKey('staff.id')

    user = relationship("User", back_populates="password_reset_code")
    staff = relationship("Staff", back_populates="password_reset_code")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)


class EmailCode(Base):
    __tablename__ = 'email_code'

    id = Column(Integer, primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    code: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)

    @classmethod
    def generate_code(cls) -> int:
        return random.randint(1000, 9999)


class Project(Base):
    __tablename__ = "project"

    name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    start_date: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), nullable=False)
    end_date: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    participants: orm.Mapped[int] = orm.mapped_column(Integer, nullable=True)
    lessons: orm.Mapped[int] = orm.mapped_column(Integer, nullable=True)
    likes: orm.Mapped[int] = orm.mapped_column(Integer, default=0)
    avatar_attachment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    avatar_attachment = relationship(
        "Attachment",
        backref="project_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )

    staff_members = relationship("ProjectStaff", back_populates="project")

    @classmethod
    def add_like(cls):
        cls.likes += 1


class ProjectStaff(Base):
    __tablename__ = "project_staff"

    project_id = Column(UUID, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="staff_members")
    staff = relationship(
        "Staff",
        back_populates="projects",
        foreign_keys=[staff_id],
        uselist=False,
    )


class ProjectLike(Base):
    __tablename__ = "project_like"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", backref="project_likes")
    staff = relationship("Staff", backref="project_likes")
    project = relationship("Project", backref="project_likes")


class News(Base):
    __tablename__ = "news"

    name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    date: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    likes: orm.Mapped[int] = orm.mapped_column(Integer, default=0)
    reminder: orm.Mapped[int] = orm.mapped_column(Integer, default=0)
    avatar_attachment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    avatar_attachment = relationship(
        "Attachment",
        backref="news_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )

    @classmethod
    def add_like(cls):
        cls.likes += 1

    @classmethod
    def add_reminder(cls):
        cls.reminder += 1


class NewsReminder(Base):
    __tablename__ = "news_reminder"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    task_id: orm.Mapped[str] = orm.mapped_column(String, nullable=True)

    user = relationship("User", backref="news_reminders")
    staff = relationship("Staff", backref="news_reminders")
    news = relationship("News", backref="news_reminders")


class NewsLike(Base):
    __tablename__ = "news_like"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", backref="news_likes")
    staff = relationship("Staff", backref="news_likes")
    news = relationship("News", backref="news_likes")


class Clip(Base):
    __tablename__ = "clip"

    id = Column(Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    date: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(String, nullable=True)
    likes: orm.Mapped[int] = orm.mapped_column(Integer, default=0)
    clip_attachment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    clip_attachment = relationship(
        "Attachment",
        backref="clip_attachment",
        foreign_keys=[clip_attachment_id],
        uselist=False,
    )

    @classmethod
    def add_like(cls):
        cls.likes += 1


class ClipLike(Base):
    __tablename__ = "clip_like"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete="CASCADE"), nullable=True)
    clip_id = Column(Integer, ForeignKey("clip.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", backref="clip_likes")
    staff = relationship("Staff", backref="clip_likes")
    clip = relationship("Clip", backref="clip_likes")
