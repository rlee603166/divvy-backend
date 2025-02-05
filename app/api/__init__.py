from fastapi import APIRouter
from .health import health_router
from .v1.router import api_v1_router

# Export the routers
__all__ = ["health_router", "api_router"]

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(api_v1_router)
