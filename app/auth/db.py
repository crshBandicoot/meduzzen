from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aioredis import from_url
from databases import Database
from os import getenv


postgres_db = Database(f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@postgres:5432/db')
postgres_engine = create_async_engine(f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@postgres:5432/db')
redis_engine = from_url('redis://redis/db', username='user', password=getenv('REDIS_PASSWORD'))
Base = declarative_base()
session = sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with session() as ses:
        yield ses
