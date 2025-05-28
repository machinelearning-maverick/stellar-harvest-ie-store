from typing import Generic, Type, TypeVar, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

T = TypeVar("T")


class AsyncRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: Any) -> Optional[T]:
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.execute(statement)
        return result.scalars().first()


    async def update(self, id: Any, **kwargs) -> T:
        read = await self.get(id)
        if not read:
            raise NoResultFound(f"{self.model.__name__}<{id}> not found")
        for key, value in kwargs.items():
            setattr(read, key, value)
        await self.session.commit()
        await self.session.refresh(read)
        return read