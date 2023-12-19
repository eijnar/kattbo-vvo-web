from sqlmodel import SQLModel, Field, Relationship
from app.models import utils
from app import models
from typing import List, Optional

class TagsCategories(models.TrackingMixin, SQLModel, table=True):
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

    
class Tag(utils.TrackingMixin, SQLModel, table=True):
    __tablename__ = 'tag'
    id: int = Field(default=None, primary_key=True, autoincrement=True)
    name: Optional[str] = Field(max_length=50)
    description: str = Field(max_length=50, nullable=False, unique=True)

    users: List["models.User"] = Relationship(
        back_populates="tags", 
        link_model=models.UsersTags
    )
    tag_category: List["models.TagCategory"] = Relationship(
        back_populates="tags", 
        link_model=models.TagsCategories
    )
    event_types: List["models.EventCategory"] = Relationship(
        back_populates="tags", 
        link_model=models.EventTypeTags
    )
    allowed_roles: List["models.Role"] = Relationship(
        back_populates="allowed_tags", 
        link_model=models.RolesTags
    )
    allowed_notification_types: List["models.NotificationType"] = Relationship(
        back_populates="tags", 
        link_model=models.TagsNotifications
    )

class TagCategory(utils.TrackingMixin, SQLModel, table=True):
    __tablename__ = 'tag_category'
    id: int = Field(default=None, primary_key=True, autoincrement=True)
    name: str = Field(max_length=50, nullable=False, unique=True)
    description: Optional[str] = Field()

    tags: List[Tag] = Relationship(back_populates='tag_category', link_model=TagsCategories)
