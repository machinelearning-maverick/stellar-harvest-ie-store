from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from stellar_harvest_ie_store.settings import settings
from stellar_harvest_ie_models.stellar.swpc.db import Base
import stellar_harvest_ie_models.stellar.swpc.entities  # noqa: F401 - registers models with Base
from stellar_harvest_ie_config.utils.log_decorators import log_io

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@log_io()
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@log_io()
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
