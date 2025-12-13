from fastapi import FastAPI

from app.core.config import get_settings
from app.api.routers import payments, health

settings = get_settings()


def get_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(health.router)
    app.include_router(payments.router, prefix=settings.API_V1_PREFIX)

    return app


app = get_app()
