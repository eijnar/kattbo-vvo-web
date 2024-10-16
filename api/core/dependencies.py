import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from repositories.user_repository import UserRepository
from .database.base import AsyncSessionLocal
from routers.users.services.user_service import UserService

logger = logging.getLogger(__name__)


async def get_db_session():
    try:
        async with AsyncSessionLocal() as session:
            yield session
            logger.debug("Database session created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error during database session creation: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error ajusted: {e}")
        raise


async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    """
    Dependency to provide an instance of UserRepository.

    Args:
        db_session (AsyncSession): The database session injected by FastAPI.

    Returns:
        UserRepository: An instance of UserRepository.
    """
    return UserRepository(db_session)

async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    """
    Dependency to provide an instance of UserService.

    Args:
        user_repository (UserRepository): The UserRepository instance injected by FastAPI.

    Returns:
        UserService: An instance of UserService.
    """
    return UserService(user_repository)