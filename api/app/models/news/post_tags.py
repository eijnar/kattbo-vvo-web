from app.models import TrackingMixin
from sqlmodel import SQLModel, Field


class PostTags(SQLModel, table=True):
    post_id: int = Field(default=None, foreign_key="post.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tag.id", primary_key=True)
