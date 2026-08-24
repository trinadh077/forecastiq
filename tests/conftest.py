import pytest
import sys
import os
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../backend')))

import app.models  # ensure models are loaded
from app.main import app as fastapi_app
from app.database.session import engine
from app.database.base_class import Base

@pytest.fixture(autouse=True)
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client
