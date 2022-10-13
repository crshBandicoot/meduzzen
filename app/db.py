from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aioredis import from_url
from os import getenv
from auth.models import Base


postgres_engine = create_async_engine(f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@postgres:5432/db')
redis_engine = from_url('redis://redis/db', username='user', password=getenv('REDIS_PASSWORD'))

session = sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with session() as ses:
        yield ses
