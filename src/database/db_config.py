from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(
    settings.db.sqal_pg_url(),
    pool_size=10,  # базовое количество открытых соединений
    max_overflow=5,  # макс. доп. соединений сверх pool_size
    pool_pre_ping=True,  # проверяет соединение перед использованием (избегает "broken pipe")
    pool_recycle=600,  # пересоздавать соединение каждые 10 минут (в секундах)
    pool_timeout=30,  # макс. время ожидания свободного соединения из пула
    # echo=False,  # отключить лог SQL (важно в production)
    connect_args={
        "command_timeout": 20,  # таймаут выполнения запроса (в секундах)
        "prepared_statement_cache_size": 100,  # кэш prepared statements (только для asyncpg)
        "statement_cache_size": 100,  # кэш запросов
        "server_settings": {"jit": "off"},  # отключить JIT (часто замедляет OLTP)
    },
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """ """
    async with AsyncSessionLocal() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
