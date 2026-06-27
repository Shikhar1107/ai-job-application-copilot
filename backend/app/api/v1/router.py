from fastapi import APIRouter

from app.api.v1.routes import health,analysis,history

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(analysis.router)
api_router.include_router(history.router)
