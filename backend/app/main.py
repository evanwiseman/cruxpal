from fastapi import FastAPI

from backend.app.api import athletes, routes
from backend.app.core.config import settings
from backend.app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

def get_with_prefix(route: str) -> str:
    return f"{settings.API_PREFIX}/{route}"


# include router under API prefix
app.include_router(
    athletes.router,
    prefix=get_with_prefix("athletes"),
    tags=["Athletes"],
)

app.include_router(
    routes.router,
    prefix=get_with_prefix("route"),
    tags=["Routes"],
)