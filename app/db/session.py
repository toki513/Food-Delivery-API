from sqlalchemy.ext.asyncio import (async_sessionmaker,AsyncSession,create_async_engine)

from app.core.config import settings


engine=create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo = settings.DEBUG,
    pool_pre_ping = True
)