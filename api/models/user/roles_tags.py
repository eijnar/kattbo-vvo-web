from models import TrackingMixin
from sqlmodel import SQLModel, Field


class RolesTags(TrackingMixin, SQLModel, table=True):
    __tablename__ = 'roles_tags'
    role_id: int = Field(
        defualt=None,
        foreign_key="role.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
    tag_id: int = Field(
        defualt=None,
        foreign_key="tag.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
