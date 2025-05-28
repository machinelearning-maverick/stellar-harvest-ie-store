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

    # Check returned object
    assert saved.id is not None
    assert saved.kp_index == 7
    assert saved.time_tag == datetime.datetime(2025, 5, 21, 12, 0, 0)

    # Confirm it's persisted
    result = await session.execute(select(KpIndexEntity))
    items = result.scalars().all()
    assert len(items) == 1
    assert items[0].kp_index == 7


@pytest.mark.asyncio
async def test_async_repository_get(session_factory):
    async with session_factory() as session:
        repository = AsyncRepository(KpIndexEntity, session)

        time_tag = datetime.datetime(2025, 5, 23, 15, 0, 0)
        created = await repository.add(KpIndexEntity(time_tag=time_tag, kp_index=4))

        read = await repository.get(created.id)

        assert read is not None
        assert read.id == created.id
        assert read.kp_index == 4
        assert read.time_tag == time_tag

        result = await session.execute(
            select(KpIndexEntity).where(KpIndexEntity.id == created.id)
        )
        fetched = result.scalars().one()
        assert fetched.kp_index == 4


@pytest.mark.asyncio
async def test_async_repository_update(session_factory):
    async with session_factory() as session:
        repository = AsyncRepository(KpIndexEntity, session)

        time_tag_original = datetime.datetime(2025, 5, 27, 10, 0, 0)
        created = await repository.add(
            KpIndexEntity(
                time_tag=time_tag_original, kp_index=2, estimated_kp=2.1, kp="1P"
            )
        )

        time_tag_updated = datetime.datetime(2025, 5, 27, 12, 30, 0)
        updated = await repository.update(
            created.id, time_tag=time_tag_updated, kp_index=5, estimated_kp=5.5, kp="3K"
        )

        assert updated.id == created.id
        assert updated.time_tag == time_tag_updated
        assert updated.kp_index == 5
        assert updated.estimated_kp == 5.5
        assert updated.kp == "3K"

        result = await session.execute(
            select(KpIndexEntity).where(KpIndexEntity.id == created.id)
        )
        fetched = result.scalars().one()
        assert fetched.kp_index == 5
        assert fetched.time_tag == time_tag_updated
        assert fetched.estimated_kp == 5.5
        assert fetched.kp == "3K"
