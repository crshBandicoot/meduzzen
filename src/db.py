from sqlalchemy.ext.asyncio import create_async_engine
from aioredis import from_url

postgres_engine = create_async_engine('postgresql+asyncpg://user:password@postgres:5432/db')
redis_engine = from_url('redis://redis/db', username='user', password='password')
