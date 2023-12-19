from app import models
from sqlmodel import SQLModel, Field

class UsersTags(models.TrackingMixin, SQLModel, table=True):
    __tablename__ = 'users_tags'
    user_id: int = Field(
        defualt=None,
        foreign_key="user.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
    tag_id: int = Field(
        defualt=None,
        foreign_key="tag.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )