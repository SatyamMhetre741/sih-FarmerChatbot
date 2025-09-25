from fastapi import APIRouter
from datetime import datetime
from app.models.schemas import HealthResponse
from app.services.gemini_service import gemini_service

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to monitor system status
    """
    # Check service statuses
    services = {
        "gemini_api": "healthy" if gemini_service.test_connection() else "unhealthy",
        "database": "healthy",  # Add actual DB health check if needed
        "weather_service": "healthy",
        "market_service": "healthy"
    }
    
    overall_status = "healthy" if all(status == "healthy" for status in services.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(),
        version="1.0.0",
        services=services
    )

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint
    """
    return {"message": "pong", "timestamp": datetime.now()}