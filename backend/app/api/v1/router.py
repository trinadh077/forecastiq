from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.datasets import router as datasets_router
from app.api.v1.endpoints.ml_models import router as ml_models_router
from app.api.v1.endpoints.forecasts import router as forecasts_router
from app.api.v1.endpoints.reports import router as reports_router
from app.api.v1.endpoints.users import router as users_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["Health"])
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
api_v1_router.include_router(datasets_router, prefix="/datasets", tags=["Datasets"])
api_v1_router.include_router(ml_models_router, prefix="/ml-models", tags=["ML Models"])
api_v1_router.include_router(forecasts_router, prefix="/forecasts", tags=["Forecasts"])
api_v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
