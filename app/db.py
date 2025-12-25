import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from typing import AsyncGenerator, Dict, Tuple

from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


_engines: Dict[int, Tuple[AsyncEngine, async_sessionmaker[AsyncSession]]] = {}


def get_engine() -> Tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    loop = asyncio.get_running_loop()
    key = id(loop)

    if key not in _engines:
        settings = get_settings()
        engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
        session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        _engines[key] = (engine, session_factory)

    return _engines[key]


async def dispose_engine() -> None:
    """Аккуратно закрыть engine именно для текущего loop."""
    loop = asyncio.get_running_loop()
    key = id(loop)
    pair = _engines.pop(key, None)
    if pair:
        engine, _ = pair
        await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    _, session_factory = get_engine()
    async with session_factory() as session:
        yield session
