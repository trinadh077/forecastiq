from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.config.logging import logger
from app.config.settings import settings
from app.core.exceptions import ForecastIQException
from app.database.session import engine
from app.database.base_class import Base
from app.core.redis import redis_service
import app.models
from app.middlewares.correlation import CorrelationIdMiddleware
from app.middlewares.logging import RequestLoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    try:
        await redis_service.connect()
    except Exception as e:
        logger.warning(f"Redis connection warning: {e}")
    yield
    await redis_service.close()
    logger.info(f"Shutting down {settings.APP_NAME}")

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

@app.api_route("/", methods=["GET", "HEAD"], tags=["Health"])
async def root():
    return {
        "message": "ForecastIQ API is running",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "api": settings.API_V1_STR,
    }

# Middlewares
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Custom Exception Handlers
@app.exception_handler(ForecastIQException)
async def forecastiq_exception_handler(request: Request, exc: ForecastIQException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": exc.errors()
            }
        }
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred."
            }
        }
    )
