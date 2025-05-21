import asyncio
import datetime

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from stellar_harvest_ie_store.db import Base, get_session
from stellar_harvest_ie_store.repository import AsyncRepository
from stellar_harvest_ie_models.stellar.swpc.entities import KpIndexEntity

pytest_plugins = ("pytest_asyncio",)


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


@pytest.mark.asyncio
async def test_async_repository_add(session_factory):
    async with session_factory() as session:
        repository = AsyncRepository(KpIndexEntity, session)
        entity = KpIndexEntity(
            time_tag=datetime.datetime(2025, 5, 21, 12, 0, 0), kp_index=7
        )
        saved = await repository.add(entity)

    assert saved.id is not None
    assert saved.kp_index == 7
    assert saved.time_tag == datetime.datetime(2025, 5, 21, 12, 0, 0)
