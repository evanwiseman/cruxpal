import asyncio

from backend.app.db.base import Base
from backend.app.db.models import *  # noqa
from backend.app.db.session import engine


async def init_db():
    async with engine.begin() as conn:
        # Drop all tables if needed (optional)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialized")
