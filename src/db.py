from sqlalchemy.ext.asyncio import create_async_engine
from aioredis import from_url
from os import getenv

postgres_engine = create_async_engine(f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:{getenv("POSTGRES_PASSWORD")}@postgres:5432/db')
redis_engine = from_url('redis://redis/db', username='user', password=getenv('REDIS_PASSWORD'))
