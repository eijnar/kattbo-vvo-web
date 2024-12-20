from logging import getLogger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError

from core.config import settings

logger = getLogger(__name__)

DATABASE_URL = settings.SQL_DATABASE_URL

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.SQL_DEBUG_MODE,
        pool_pre_ping=True
    )
    logger.info("Async engine created successfully.")
except SQLAlchemyError as e:
    logger.error(f"Error creating async engine: {e}")
    raise

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base: DeclarativeMeta = declarative_base()


async def create_tables():
    logger.debug("Creating database tables.")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Database tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
