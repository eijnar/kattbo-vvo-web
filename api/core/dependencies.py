import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.database.base import AsyncSessionLocal
from core.security.security_repository import SecurityRepository
from core.security.security_service import SecurityService
from repositories import (
    UserRepository,
    TeamRepository,
    UserTeamAssignmentRepository,
    HuntingYearRepository,
    EventRepository,
    EventDayRepository,
    EventDayGatheringRepository,
    EventCategoryRepository,
    WaypointRepository,
)
from services import (
    UserService,
    TeamService,
    UserTeamAssignmentService,
    HuntingYearService,
    EventService,
    WaypointService
)


logger = logging.getLogger(__name__)


async def get_db_session():
    logger.debug(
        "get_db_session: Attempting to create a new database session.")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            logger.debug("Database session created successfully.")
        except SQLAlchemyError as e:
            logger.error(f"Error during database session creation: {e}")
            await session.rollback()
            raise
    logger.debug("Database session closed successfully.")


# Repositories

async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    logger.debug("get_user_repository")
    return UserRepository(db_session)


async def get_team_repository(db_session: AsyncSession = Depends(get_db_session)) -> TeamRepository:
    logger.debug("get_team_repository")
    return TeamRepository(db_session)


async def get_security_repository(db_session: AsyncSession = Depends(get_db_session)) -> SecurityRepository:
    logger.debug("get_security_repository")
    return SecurityRepository(db_session)


async def get_user_team_assignment_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserTeamAssignmentRepository:
    logger.debug("get_user_team_assignment_repository")
    return UserTeamAssignmentRepository(db_session)


async def get_hunting_year_repository(db_session: AsyncSession = Depends(get_db_session)) -> HuntingYearRepository:
    logger.debug("get_hunting_year_repository")
    return HuntingYearRepository(db_session)


async def get_event_repository(db_session: AsyncSession = Depends(get_db_session)) -> EventRepository:
    logger.debug("get_event_repository")
    return EventRepository(db_session)


async def get_event_day_repository(db_session: AsyncSession = Depends(get_db_session)) -> EventDayRepository:
    logger.debug("get_event_day_repository")
    return EventDayRepository(db_session)


async def get_event_day_gathering_repository(db_session: AsyncSession = Depends(get_db_session)) -> EventDayGatheringRepository:
    logger.debug("get_event_day_gathering_repository")
    return EventDayGatheringRepository(db_session)


async def get_event_category_repository(db_session: AsyncSession = Depends(get_db_session)) -> EventCategoryRepository:
    logger.debug("get_event_category_repository")
    return EventCategoryRepository(db_session)


async def get_waypoint_repository(db_session: AsyncSession = Depends(get_db_session)) -> WaypointRepository:
    logger.debug("get_waypoint_repository")
    return WaypointRepository(db_session)


# Services

async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    logger.debug("get_user_service")
    return UserService(user_repository)


def get_waypoint_service(
    waypoint_repository: WaypointRepository = Depends(get_waypoint_repository)
) -> WaypointService:
    logger.debug("get_waypoint_service")
    return WaypointService(waypoint_repository)


async def get_hunting_year_service(
    db_session: AsyncSession = Depends(get_db_session)
) -> HuntingYearService:
    repository = HuntingYearRepository(db_session)
    return HuntingYearService(repository)


async def get_team_service(
    team_repository: TeamRepository = Depends(get_team_repository),
    user_team_assignment_repository: UserTeamAssignmentRepository = Depends(
        get_user_team_assignment_repository),
    hunting_year_service: HuntingYearService = Depends(
        get_hunting_year_service),
) -> TeamService:
    logger.debug("get_user_service")
    return TeamService(team_repository, user_team_assignment_repository, hunting_year_service)


def get_security_service(
    security_repository: SecurityRepository = Depends(get_security_repository),
    user_service: UserService = Depends(get_user_service),
) -> SecurityService:
    return SecurityService(security_repository, user_service)


def get_user_team_assignment_service(
    user_team_assignment_repository: UserTeamAssignmentRepository = Depends(
        get_user_team_assignment_repository),
    team_service: TeamService = Depends(get_team_service),
    user_service: UserService = Depends(get_user_service),
    hunting_year_service: HuntingYearService = Depends(
        get_hunting_year_service)
) -> UserTeamAssignmentService:
    return UserTeamAssignmentService(user_team_assignment_repository, team_service, user_service, hunting_year_service)


def get_event_service(
    event_repository: EventRepository = Depends(get_event_repository),
    event_day_repository: EventDayRepository = Depends(
        get_event_day_repository),
    event_day_gathering_repository: EventDayGatheringRepository = Depends(
        get_event_day_gathering_repository),
    event_category_repository: EventCategoryRepository = Depends(
        get_event_category_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    team_repository: TeamRepository = Depends(get_team_repository),
    waypoint_repository: WaypointRepository = Depends(get_waypoint_repository),
) -> EventService:
    
    return EventService(
        event_repository,
        event_day_repository,
        event_day_gathering_repository,
        event_category_repository,
        user_repository,
        team_repository,
        waypoint_repository
    )