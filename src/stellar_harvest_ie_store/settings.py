import logging

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

DATABASE_URL = "DATABASE_URL"


class StoreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None)

    database_url: str = Field(
        "postgresql+asyncpg://postgres:PAssw0rd@postgres:5432/stellar_harvest_ie_db",
        env=DATABASE_URL,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("StoreSettings()")


settings = StoreSettings()
