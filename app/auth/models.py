from sqlalchemy import Column, String, Integer, MetaData
from .db import Base, postgres_engine
import asyncio


metadata = MetaData()


class User(Base):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True, index=True)
    user = Column('username', String, unique=True, index=True)
    email = Column('user_email', String, unique=True, index=True)
    password = Column('user_password', String)


async def init_models():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

