from uuid import uuid4

from sqlalchemy import Column, Integer, String, UUID, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from core.database import Base
from models.dependencies import TrackingMixin, CRUDMixin

roles_users = Table('roles_users', Base.metadata,
                    Column('user_id', Integer, ForeignKey(
                        'user.id'), primary_key=True),
                    Column('role_id', Integer, ForeignKey(
                        'role.id'), primary_key=True)
                    )


class UserModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    hashed_password = Column(String(420))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    profile_picture = Column(String(255), default='profile_pics/default.png')
    active = Column(Boolean, default=True)

    # Relationships
    roles = relationship('RoleModel', secondary=roles_users, back_populates='users')
    
class RoleModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    description = Column(String(255))
    
    # Relationships
    users = relationship('UserModel', secondary=roles_users, back_populates='roles')