import requests
import logging
from typing import Optional
from app.config import get_settings
from app.models.schemas import WeatherInfo
from datetime import datetime

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather information"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather_info(self, location: str) -> Optional[WeatherInfo]:
        """Get weather information for a location"""
        try:
            if not self.settings.weather_api_key:
                logger.warning("Weather API key not configured")
                return None
            
            params = {
                'q': location,
                'appid': self.settings.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return WeatherInfo(
                location=data['name'],
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                rainfall=data.get('rain', {}).get('1h', 0.0),
                description=data['weather'][0]['description']
            )
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return None

class MarketService:
    """Service for market price information"""
    
    def __init__(self):
        self.settings = get_settings()
    
    async def get_market_prices(self, crop: str, location: str = "india") -> dict:
        """Get market prices for a crop (mock implementation)"""
        # This is a mock implementation
        # In production, integrate with actual market APIs like:
        # - eNAM (National Agriculture Market)
        # - AGMARKNET
        # - State agriculture department APIs
        
        mock_prices = {
            "wheat": {"price_per_kg": 25.50, "trend": "stable"},
            "rice": {"price_per_kg": 45.00, "trend": "increasing"},
            "tomato": {"price_per_kg": 30.00, "trend": "decreasing"},
            "potato": {"price_per_kg": 18.00, "trend": "stable"},
            "onion": {"price_per_kg": 35.00, "trend": "increasing"},
        }
        
        crop_lower = crop.lower()
        if crop_lower in mock_prices:
            return {
                "crop": crop,
                "location": location,
                "price_per_kg": mock_prices[crop_lower]["price_per_kg"],
                "trend": mock_prices[crop_lower]["trend"],
                "last_updated": datetime.now().isoformat(),
                "source": "Mock Market API"
            }
        else:
            return {
                "crop": crop,
                "location": location,
                "message": f"Price information for {crop} not available",
                "suggestion": "Contact local mandi for current prices"
            }

# Service instances
weather_service = WeatherService()
market_service = MarketService()