from sqlmodel import SQLModel, Field, Relationship
from app.models import utils
from app import models
from typing import List, Optional
from datetime import datetime


class RolesUsers(utils.TrackingMixin, SQLModel, table=True):
    __tablename__ = 'roles_users'
    role_id: int = Field(
        defualt=None,
        foreign_key="role.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
    role_id: int = Field(
        defualt=None,
        foreign_key="user.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )







class User(utils.TrackingMixin, SQLModel, table=True):
    # Flask-Security-Too specific columns
    id: int = Field(default=None, primary_key=True)
    username: Optional[str] = Field(max_length=255)
    password: Optional[str] = Field(max_length=255)
    email: str = Field(max_length=255)
    active: bool = Field()
    fs_uniquifier: Optional[str] = Field(max_length=64)
    fs_webauthn_user_handle: Optional[str] = Field(max_length=64)
    mf_recovery_codes: Optional[str] = Field()
    us_phone_number: Optional[str] = Field(max_length=128)
    us_totp_secrets: Optional[str] = Field()
    confirmed_at: Optional[datetime] = Field()
    last_login_ip: Optional[str] = Field(max_length=64)
    current_login_ip: Optional[str] = Field(max_length=64)
    login_count: Optional[int] = Field()
    tf_primary_method: Optional[str] = Field(max_length=64)
    tf_totp_secret: Optional[str] = Field(max_length=255)
    tf_phone_number: Optional[str] = Field(max_length=128)

    # Custom columns
    first_name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=255)
    profile_picture: Optional[str] = Field(max_length=255)

    # Many-to-Many Relationships
    roles: List["Role"] = Relationship(
        back_populates="users", link_model=RolesUsers)
    tags: List["models.Tag"] = Relationship(
        back_populates="tag_users", link_model=UsersTags)

    # One-to-Many Relationships
    users_events: List["models.UsersEvents"] = Relationship(
        back_populates="user"
    )
    created_events: List["models.Event"] = Relationship(
        back_populates="creator"
    )
    general_preferences: List["models.UserPreference"] = Relationship(
        back_populates="preference_user"
    )
    notification_preferences: List["models.UserNotificationPreference"] = Relationship(
        back_populates="user_notification_preferences"
    )
    hunt_years: List["models.UserTeamYear"] = Relationship(
        back_populates="user"
    )
    stand_assignments: List["models.StandAssignment"] = Relationship(
        back_populates="user"
    )
    posts: List["models.Post"] = Relationship(
        back_populates="author"
    )
