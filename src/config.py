from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class DataBaseConfig(BaseSettings):
    """ """

    user: Annotated[str | None, Field(alias="POSTGRES_USER")] = None
    password: Annotated[str | None, Field(alias="POSTGRES_PASSWORD")] = None
    host: Annotated[str | None, Field(alias="POSTGRES_HOST")] = None
    port: Annotated[int | None, Field(alias="POSTGRES_PORT")] = None
    dbname: Annotated[str | None, Field(alias="POSTGRES_DB")] = None
    driver: str = "asyncpg"
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")

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
    """  """
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.test", env_file_encoding="utf-8")


class Settings(BaseModel):
    """ """

    db: DataBaseConfig = DataBaseConfig()
    dbtest: DataBaseTestConfig = DataBaseTestConfig()


settings = Settings()
