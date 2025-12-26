from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class DataBaseConfig(BaseSettings):
    """ """

    user: Annotated[str | None, Field(alias="POSTGRES_USER")] = None
    password: Annotated[str | None, Field(alias="POSTGRES_PASSWORD")] = None
    host: Annotated[str, Field(alias="POSTGRES_HOST")] = "db"
    port: Annotated[int, Field(ge=1024, le=65535, alias="POSTGRES_PORT")] = 5432
    dbname: Annotated[str | None, Field(alias="POSTGRES_DB")] = None
    driver: str = "asyncpg"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def sqal_pg_url(
        self,
        driver_override: str | None = None,
        host_override: str | None = None,
        port_override: int | None = None,
    ) -> str:
        """ """
        driver = driver_override or self.driver
        host = host_override or self.host
        port = port_override or self.port
        return f"postgresql+{driver}://{self.user}:{self.password}@{host}:{port}/{self.dbname}"


class DataBaseTestConfig(DataBaseConfig):
    """ """

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.test", env_file_encoding="utf-8")


class RedisConfig(BaseSettings):
    """ """

    password: Annotated[str | None, Field(alias="REDIS_PASSWORD")] = None
    host: Annotated[str, Field(alias="REDIS_HOST")] = "localhost"
    port: Annotated[int, Field(alias="REDIS_PORT")] = 6379
    db: int = 0
    short_url_limit: int = 3
    short_url_window: int = 5

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class RedisTestConfig(BaseSettings):
    """ """

    password: Annotated[str | None, Field(alias="REDIS_PASSWORD")] = None
    host: Annotated[str, Field(alias="REDIS_HOST")] = "localhost"
    port: Annotated[int, Field(alias="REDIS_PORT")] = 6378
    db: int = 0
    short_url_limit: int = 3
    short_url_window: int = 5

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.test",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings(BaseModel):
    """ """

    db: DataBaseConfig = DataBaseConfig()
    dbtest: DataBaseTestConfig = DataBaseTestConfig()
    redis_db: RedisConfig = RedisConfig()
    redis_test: RedisTestConfig = RedisTestConfig()


settings = Settings()
