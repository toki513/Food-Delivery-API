from sqlalchemy.ext.asyncio import (async_sessionmaker,AsyncSession,create_async_engine)

from app.core.config import settings


engine=create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo = settings.DEBUG,
    pool_pre_ping = True
)

AsyncSessionLocal=async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db()-> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session 
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()