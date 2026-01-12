from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# Async engine (use aiosqlite for SQLite dev or async Postgres)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
)

# Async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency for FastAPI routes
async def get_db():
    async with async_session() as session:
        yield session
