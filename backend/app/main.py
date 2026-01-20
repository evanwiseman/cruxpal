from fastapi import FastAPI

from backend.app.api import ascents, athletes, auth, routes
from backend.app.core.config import settings
from backend.app.core.endpoints import endpoints
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


# include router under API prefix
app.include_router(
    athletes.router,
    prefix=endpoints.ATHLETES_BASE,
    tags=["Athletes"],
)

app.include_router(
    routes.router,
    prefix=endpoints.ROUTES_BASE,
    tags=["Routes"],
)

app.include_router(
    ascents.router,
    prefix=endpoints.ASCENTS_BASE,
    tags=["Ascents"],
)

app.include_router(
    auth.router,
    prefix=endpoints.AUTH_BASE,
    tags=["Auth"],
)