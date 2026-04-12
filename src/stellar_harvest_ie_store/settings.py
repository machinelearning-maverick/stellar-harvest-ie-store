import logging

from pydantic import Field
from stellar_harvest_ie_config.logging_config import setup_logging
from pydantic_settings import BaseSettings, SettingsConfigDict

setup_logging()
logger = logging.getLogger(__name__)

DATABASE_URL = "DATABASE_URL"


class StoreSettings(BaseSettings):
    logger.info("StoreSettings()")

    model_config = SettingsConfigDict(env_file=None)

    database_url: str = Field(
        "postgresql+asyncpg://postgres:PAssw0rd@postgres:5432/stellar_harvest_ie_db",
        env=DATABASE_URL,
    )


settings = StoreSettings()
