"""
Simple test script to verify the FastAPI application setup
Run this after setting up your environment to ensure everything works
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_basic_functionality():
    """Test basic functionality without requiring API keys"""
    print("🧪 Testing AI Farmer Query Support System Setup...")
    print("=" * 50)
    
    # Test 1: Import all modules
    try:
        from app.config import get_settings
        from app.models.schemas import FarmerQueryRequest, QueryCategory
        from app.services.additional_services import weather_service, market_service
        print("✅ All modules imported successfully")
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    # Test 2: Configuration
    try:
        settings = get_settings()
        print(f"✅ Configuration loaded (Debug: {settings.debug})")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False
    
    # Test 3: Pydantic models
    try:
        request = FarmerQueryRequest(
            query="How to grow tomatoes?",
            location="Maharashtra",
            crop_type="tomato"
        )
        print(f"✅ Pydantic models working: {request.query}")
    except Exception as e:
        print(f"❌ Pydantic models failed: {e}")
        return False
    
    # Test 4: Market service (mock)
    try:
        price_info = await market_service.get_market_prices("tomato", "mumbai")
        print(f"✅ Market service working: {price_info['crop']}")
    except Exception as e:
        print(f"❌ Market service failed: {e}")
        return False
    
    print("\n🎉 Basic setup verification complete!")
    print("\nNext steps:")
    print("1. Add your GEMINI_API_KEY to .env file")
    print("2. Run: python -m uvicorn main:app --reload")
    print("3. Visit: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())