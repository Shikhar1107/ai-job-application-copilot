from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

from app.db.base import Base
from app.db.models import AnalysisRun
from app.db.session import engine

def create_app() -> FastAPI:
    app = FastAPI(
        title= settings.APP_NAME,
        version="0.1.0",
        description="Backend API for AI Job Application Copilot"
    )
    cors_origins = settings.cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins = cors_origins,
        allow_credentials=False if cors_origins == ["*"] else True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    # Base.metadata.create_all(bind=engine)
    return app

app =create_app()