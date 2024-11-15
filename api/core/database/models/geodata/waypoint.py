import uuid
from typing import Optional

from sqlalchemy import Index, Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

from core.database.base import Base
from core.database.models.geodata.waypoint_area import waypoint_areas
from core.database.mixins import TrackingMixin, SoftDeleteMixin

class Waypoint(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'waypoints'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326, nullable=False))
    category_id = Column(UUID(as_uuid=True), ForeignKey('waypoint_categories.id'), nullable=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)

    # Relationships
    category = relationship('WaypointCategory', back_populates='waypoints', lazy='selectin')
    team = relationship('Team', back_populates='waypoints')
    areas = relationship(
        'Area',
        secondary=waypoint_areas,
        back_populates='waypoints'
    )
    stand_assignments = relationship('WaypointStandAssignment', back_populates='waypoint', cascade='all, delete-orphan')
    tasks = relationship('WaypointTask', back_populates='waypoint', cascade='all, delete-orphan')
    event_day_gathering_places = relationship('EventDayGatheringPlace', back_populates='gathering_place', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_waypoints_location_v2', 'location', postgresql_using='gist'),
    )
    
    @property
    def latitude(self) -> Optional[float]:
        if self.location:
            point = to_shape(self.location)
            return point.y
        return None

    @property
    def longitude(self) -> Optional[float]:
        if self.location:
            point = to_shape(self.location)
            return point.x
        return None