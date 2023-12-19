from models import TrackingMixin
from sqlmodel import SQLModel, Field


class TagsCategories(TrackingMixin, SQLModel, table=True):
    __tablename__ = 'tags_categories'
    tag_id: int = Field(
        defualt=None,
        foreign_key="tag.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
    tag_category_id: int = Field(
        default=None,
        foreign_key="tag_category.id",
        primary_key=True,
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
