import logging
from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class StoreSettings(BaseSettings):
    logger.info("StoreSettings()")

    model_config = SettingsConfigDict(env_file=".env")

    database_url: str


settings = StoreSettings()
