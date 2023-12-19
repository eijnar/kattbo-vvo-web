from app.models import TrackingMixin, TagsCategories
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class TagCategory(TrackingMixin, SQLModel, table=True):
    __tablename__ = 'tag_category'
    id: int = Field(default=None, primary_key=True, autoincrement=True)
    name: str = Field(max_length=50, nullable=False, unique=True)
    description: Optional[str] = Field()

    tags: List[Tag] = Relationship(back_populates='tag_category', link_model=TagsCategories)