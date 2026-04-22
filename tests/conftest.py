import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from stellar_harvest_ie_models.base import Base

@pytest_asyncio.fixture(loop_scope="module")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory(engine):
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
def override_get_session(monkeypatch, session_factory):
    async def _get_session():
        async with session_factory() as session:
            yield session

    monkeypatch.setattr("stellar_harvest_ie_store.db.get_session", _get_session)