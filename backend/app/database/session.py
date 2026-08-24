from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.settings import settings

# Build DATABASE_URL from components if not set directly
db_url = settings.DATABASE_URL
if not db_url or db_url.strip() == "":
    # Fallback: build from individual settings
    db_url = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Ensure async driver
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Handle SSL for Neon/Render PostgreSQL — asyncpg uses ssl parameter, not sslmode
import ssl as _ssl
connect_args = {}
if "sqlite" in db_url:
    connect_args["check_same_thread"] = False
else:
    # For PostgreSQL: remove unsupported params from URL and configure SSL via connect_args
    for param in ["sslmode=require", "channel_binding=require"]:
        db_url = db_url.replace(param, "")
    db_url = db_url.replace("?&", "?").replace("&&", "&").replace("&&", "&")
    db_url = db_url.rstrip("?").rstrip("&")
    connect_args["ssl"] = _ssl.create_default_context()

engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    connect_args=connect_args,
    pool_size=5,
    max_overflow=10,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
