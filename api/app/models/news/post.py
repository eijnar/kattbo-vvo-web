from sqlmodel import SQLModel, Field, Relationship
from app.models import TrackingMixin, Tag
from typing import List


class Post(TrackingMixin, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_lenght=100)
    content: str = Field()
    user_id: int = Field(foreign_key="user.id")
    tags: List[Tag] = Relationship(back_populates="posts", link_model=PostTags)