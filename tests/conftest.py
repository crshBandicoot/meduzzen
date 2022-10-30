import pytest
from main import app
from httpx import AsyncClient
from db import postgres_engine
from models import Base


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url='http://localhost:8000', headers={'Content-Type': 'application/json'}) as client:
        yield client


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session')
async def refresh_db():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
