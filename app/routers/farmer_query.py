import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional
from app.models.schemas import (
    FarmerQueryRequest, 
    FarmerQueryResponse,
    VoiceQueryRequest,
    ImageQueryRequest,
    QueryCategory
)
from app.services.gemini_service import gemini_service
from app.services.additional_services import weather_service, market_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/ask", response_model=FarmerQueryResponse)
async def ask_farmer_question(request: FarmerQueryRequest):
    """
    Main endpoint for farmer text queries
    """
    try:
        logger.info(f"Received farmer query: {request.query[:100]}...")
        
        # Prepare farmer context
        farmer_context = {
            "location": request.location,
            "crop_type": request.crop_type,
            "farmer_id": request.farmer_id
        }
        
        # Process query with Gemini
        response = await gemini_service.process_farmer_query(
            query=request.query,
            category=request.category,
            farmer_context=farmer_context
        )
        
        logger.info(f"Successfully processed query for farmer {request.farmer_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing farmer query: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your query. Please try again."
        )

@router.get("/ask-simple")
async def ask_simple_question(
    query: str = Query(..., description="Your farming question"),
    location: Optional[str] = Query(None, description="Your location"),
    crop: Optional[str] = Query(None, description="Crop type"),
    category: Optional[QueryCategory] = Query(None, description="Query category")
):
    """
    Simplified GET endpoint for basic queries (useful for testing)
    """
    try:
        farmer_context = {
            "location": location,
            "crop_type": crop,
            "farmer_id": None
        }
        
        response = await gemini_service.process_farmer_query(
            query=query,
            category=category,
            farmer_context=farmer_context
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing simple query: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your query. Please try again."
        )

@router.post("/ask-voice")
async def ask_voice_question(request: VoiceQueryRequest):
    """
    Endpoint for voice-based queries (Future implementation)
    """
    # TODO: Implement voice processing using Whisper API
    # 1. Decode base64 audio
    # 2. Convert speech to text using Whisper
    # 3. Process text query with Gemini
    # 4. Convert response back to speech (optional)
    
    return {
        "message": "Voice processing feature coming soon!",
        "status": "not_implemented",
        "suggestion": "Please use the text query endpoint for now"
    }

@router.post("/ask-image")
async def ask_image_question(request: ImageQueryRequest):
    """
    Endpoint for image-based queries (pest/disease identification)
    """
    # TODO: Implement image processing
    # 1. Decode base64 image
    # 2. Use ResNet50 or similar for pest/disease identification
    # 3. Combine image analysis with text query
    # 4. Get treatment recommendations from Gemini
    
    return {
        "message": "Image analysis feature coming soon!",
        "status": "not_implemented",
        "suggestion": "Please describe your pest/disease issue in text for now"
    }

@router.get("/weather")
async def get_weather_info(location: str = Query(..., description="Location name")):
    """
    Get weather information for farming decisions
    """
    try:
        weather_info = await weather_service.get_weather_info(location)
        
        if not weather_info:
            raise HTTPException(
                status_code=404,
                detail=f"Weather information not available for {location}"
            )
        
        return weather_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching weather info: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch weather information"
        )

@router.get("/market-price")
async def get_market_price(
    crop: str = Query(..., description="Crop name"),
    location: str = Query("india", description="Market location")
):
    """
    Get current market prices for crops
    """
    try:
        price_info = await market_service.get_market_prices(crop, location)
        return price_info
        
    except Exception as e:
        logger.error(f"Error fetching market price: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch market price information"
        )

@router.get("/categories")
async def get_query_categories():
    """
    Get available query categories
    """
    return {
        "categories": [
            {"value": "crop_management", "label": "Crop Management"},
            {"value": "pest_disease", "label": "Pest & Disease Control"},
            {"value": "weather", "label": "Weather & Seasonal Advice"},
            {"value": "market_price", "label": "Market Prices"},
            {"value": "soil_health", "label": "Soil Health"},
            {"value": "irrigation", "label": "Irrigation & Water Management"},
            {"value": "fertilizer", "label": "Fertilizer & Nutrients"},
            {"value": "general", "label": "General Farming"}
        ]
    }

@router.get("/test-gemini")
async def test_gemini_connection():
    """
    Test endpoint to check Gemini API connection
    """
    try:
        is_connected = gemini_service.test_connection()
        
        if is_connected:
            return {
                "status": "success",
                "message": "Gemini API is working correctly",
                "api_available": True
            }
        else:
            return {
                "status": "error",
                "message": "Gemini API connection failed",
                "api_available": False
            }
            
    except Exception as e:
        logger.error(f"Error testing Gemini connection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API test failed: {str(e)}"
        )