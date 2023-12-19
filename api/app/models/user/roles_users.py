from app.models import TrackingMixin
from sqlmodel import SQLModel, Field


class RolesUsers(TrackingMixin, SQLModel, table=True):
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
