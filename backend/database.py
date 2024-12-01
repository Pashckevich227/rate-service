from typing import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings
from models import *


DATABASE_URL = (f"postgresql+asyncpg://"
                f"{settings.POSTGRES_USER}:"
                f"{settings.POSTGRES_PASSWORD}@"
                f"{settings.POSTGRES_HOST}/"
                f"{settings.POSTGRES_DATABASE}")


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = None
    try:
        session = async_session_maker()
        async with session as session:
            yield session
    finally:
        if session is not None:
            await session.close()


async def test_connection(session: AsyncSession):
    """
    Проверка доступа в базу
    """
    try:
        await session.execute(select(1))
    except RuntimeError as e:
        print("Error:", e)