from typing import Any, AsyncGenerator, Generator

from httpx import ASGITransport, AsyncClient
import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings
from src.core import get_redis
from src.database import Base, get_async_session
from src.main import app

engine = create_async_engine(
    settings.dbtest.sqal_pg_url(),
    poolclass=NullPool,  # важно для тестов!
)

TestAsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as sess:
        yield sess
        await sess.rollback()


def get_test_redis() -> Redis:
    return Redis(
        host=settings.redis_test.host,
        port=settings.redis_test.port,
        password=settings.redis_test.password,
    )


@pytest.fixture(scope="function", autouse=True)
async def setup_test_redis() -> AsyncGenerator[Redis, None]:
    r = get_test_redis()
    await r.ping()  # type: ignore
    await r.flushdb()
    yield r
    await r.aclose()


@pytest.fixture(autouse=True)
def override_dependencies(
    session: AsyncSession,
    setup_test_redis: Redis,
) -> Generator[None, Any, None]:
    app.dependency_overrides[get_async_session] = lambda: session
    app.dependency_overrides[get_redis] = lambda: setup_test_redis
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_async_session, None)
        app.dependency_overrides.pop(get_redis, None)


@pytest.fixture(scope="session", autouse=True)
async def setup_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
