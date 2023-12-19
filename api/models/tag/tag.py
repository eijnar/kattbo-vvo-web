from sqlmodel import SQLModel, Field, Relationship
from models import TagCategory, UsersTags, TagsCategories, EventTypeTags, RolesTags, TagsNotifications
from typing import List, Optional


class Tag(utils.TrackingMixin, SQLModel, table=True):
    __tablename__ = 'tag'
    id: int = Field(default=None, primary_key=True, autoincrement=True)
    name: Optional[str] = Field(max_length=50)
    description: str = Field(max_length=50, nullable=False, unique=True)

    users: List["User"] = Relationship(
        back_populates="tags",
        link_model=UsersTags
    )
    tag_category: List["TagCategory"] = Relationship(
        back_populates="tags",
        link_model=TagsCategories
    )
    event_types: List["EventCategory"] = Relationship(
        back_populates="tags",
        link_model=EventTypeTags
    )
    allowed_roles: List["Role"] = Relationship(
        back_populates="allowed_tags",
        link_model=RolesTags
    )
    allowed_notification_types: List["NotificationType"] = Relationship(
        back_populates="tags",
        link_model=TagsNotifications
    )
