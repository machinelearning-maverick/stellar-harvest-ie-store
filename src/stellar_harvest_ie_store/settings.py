import logging
from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

DATABASE_URL = "DATABASE_URL"


class StoreSettings(BaseSettings):
    logger.info("StoreSettings()")

    model_config = SettingsConfigDict(env_file=None)

    database_url: str = Field("postgresql+asyncpg://app:secret@postgres/ui_db")


settings = StoreSettings()
