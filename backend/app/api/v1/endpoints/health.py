from fastapi import APIRouter
from app.schemas.common import GenericResponse

router = APIRouter()

@router.get("/health", response_model=GenericResponse[dict])
async def health_check():
    return GenericResponse(
        success=True,
        message="ForecastIQ API Service is healthy",
        data={"status": "online", "version": "1.0.0"}
    )
