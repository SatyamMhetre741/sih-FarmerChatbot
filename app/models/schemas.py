from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class QueryType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"

class QueryCategory(str, Enum):
    CROP_MANAGEMENT = "crop_management"
    PEST_DISEASE = "pest_disease"
    WEATHER = "weather"
    MARKET_PRICE = "market_price"
    SOIL_HEALTH = "soil_health"
    IRRIGATION = "irrigation"
    FERTILIZER = "fertilizer"
    GENERAL = "general"

class FarmerQueryRequest(BaseModel):
    query: str = Field(..., description="Farmer's query text")
    query_type: QueryType = QueryType.TEXT
    category: Optional[QueryCategory] = None
    farmer_id: Optional[str] = None
    location: Optional[str] = None
    crop_type: Optional[str] = None
    language: str = Field(default="english", description="Response language preference")

class FarmerQueryResponse(BaseModel):
    answer: str = Field(..., description="AI-generated response")
    confidence_score: float = Field(..., description="Confidence level of the response")
    category: QueryCategory
    suggestions: List[str] = Field(default=[], description="Additional suggestions")
    sources: List[str] = Field(default=[], description="Information sources")
    timestamp: datetime

class VoiceQueryRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio")
    farmer_id: Optional[str] = None
    location: Optional[str] = None

class ImageQueryRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image")
    query: Optional[str] = Field(None, description="Additional text query about the image")
    farmer_id: Optional[str] = None
    location: Optional[str] = None

class WeatherInfo(BaseModel):
    location: str
    temperature: float
    humidity: float
    rainfall: float
    description: str

class MarketPrice(BaseModel):
    crop: str
    price_per_kg: float
    market_location: str
    date: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    services: dict