from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from stellar_harvest_ie_store.settings import settings
from stellar_harvest_ie_models.stellar.swpc.db import Base

from stellar_harvest_ie_config.utils.log_decorators import log_io
from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


from pydantic_settings import BaseSettings, SettingsConfigDict


@log_io()
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@log_io()
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
