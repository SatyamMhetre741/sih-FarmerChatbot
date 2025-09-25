import os
import logging
import json
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from app.config import get_settings
from app.models.schemas import QueryCategory, FarmerQueryResponse
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for handling Gemini API interactions"""
    
    def __init__(self):
        self.settings = get_settings()
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Gemini LLM"""
        try:
            if not self.settings.gemini_api_key or self.settings.gemini_api_key == "your_gemini_api_key_here":
                raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY in .env file")
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=self.settings.gemini_api_key,
                temperature=0.7,
                max_tokens=1000
            )
            logger.info("✅ Gemini LLM initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini LLM: {e}")
            raise
    
    def _create_system_prompt(self, category: Optional[QueryCategory] = None) -> str:
        """Create system prompt based on query category"""
        base_prompt = """You are an expert agricultural advisor AI assistant designed to help farmers in India. 
        You provide practical, actionable advice based on scientific farming practices and local conditions.

        Guidelines:
        1. Give specific, actionable advice
        2. Consider Indian farming conditions and practices
        3. Mention relevant crops, seasons, and regional factors
        4. Include cost-effective solutions
        5. Provide safety warnings when discussing pesticides/chemicals
        6. Suggest organic/sustainable alternatives when possible
        7. Keep responses concise but comprehensive
        8. If unsure, recommend consulting local agricultural extension officers"""
        
        category_specific = {
            QueryCategory.CROP_MANAGEMENT: "\nFocus on: Crop cultivation, planting techniques, harvesting, yield improvement.",
            QueryCategory.PEST_DISEASE: "\nFocus on: Pest identification, disease management, organic treatments, IPM strategies.",
            QueryCategory.WEATHER: "\nFocus on: Weather-related farming advice, seasonal planning, climate adaptation.",
            QueryCategory.MARKET_PRICE: "\nFocus on: Market trends, price forecasting, best selling practices.",
            QueryCategory.SOIL_HEALTH: "\nFocus on: Soil testing, nutrient management, soil conservation.",
            QueryCategory.IRRIGATION: "\nFocus on: Water management, irrigation methods, water conservation.",
            QueryCategory.FERTILIZER: "\nFocus on: Nutrient management, fertilizer application, organic alternatives."
        }
        
        if category and category in category_specific:
            base_prompt += category_specific[category]
        
        return base_prompt
    
    def _determine_category(self, query: str) -> QueryCategory:
        """Determine query category based on keywords"""
        query_lower = query.lower()
        
        # Keywords for each category
        keywords = {
            QueryCategory.PEST_DISEASE: ['pest', 'disease', 'insect', 'fungus', 'virus', 'infection', 'spots', 'worm', 'aphid'],
            QueryCategory.CROP_MANAGEMENT: ['planting', 'harvesting', 'cultivation', 'growing', 'yield', 'variety', 'seed'],
            QueryCategory.WEATHER: ['weather', 'rain', 'temperature', 'season', 'monsoon', 'drought', 'flood'],
            QueryCategory.SOIL_HEALTH: ['soil', 'nutrients', 'ph', 'organic matter', 'testing', 'fertility'],
            QueryCategory.IRRIGATION: ['water', 'irrigation', 'watering', 'drip', 'sprinkler', 'drought'],
            QueryCategory.FERTILIZER: ['fertilizer', 'nutrients', 'nitrogen', 'phosphorus', 'potassium', 'manure'],
            QueryCategory.MARKET_PRICE: ['price', 'market', 'selling', 'cost', 'profit', 'revenue']
        }
        
        for category, words in keywords.items():
            if any(word in query_lower for word in words):
                return category
        
        return QueryCategory.GENERAL
    
    def _calculate_confidence(self, response: str, query: str) -> float:
        """Calculate confidence score based on response quality"""
        # Simple confidence calculation based on response length and specificity
        confidence = 0.7  # Base confidence
        
        if len(response) > 100:
            confidence += 0.1
        if any(word in response.lower() for word in ['recommend', 'suggest', 'should', 'can']):
            confidence += 0.1
        if any(word in response.lower() for word in ['kg/acre', 'ml/liter', 'days', 'weeks']):
            confidence += 0.1
            
        return min(confidence, 1.0)
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract additional suggestions from response"""
        suggestions = []
        
        # Look for numbered points or bullet points
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*')) or (line and line[0].isdigit() and '.' in line):
                suggestion = line.lstrip('•-*0123456789. ')
                if suggestion and len(suggestion) > 10:
                    suggestions.append(suggestion)
        
        return suggestions[:3]  # Return top 3 suggestions
    
    async def process_farmer_query(
        self, 
        query: str, 
        category: Optional[QueryCategory] = None,
        farmer_context: Optional[dict] = None
    ) -> FarmerQueryResponse:
        """Process farmer query using Gemini API"""
        try:
            # Determine category if not provided
            if not category:
                category = self._determine_category(query)
            
            # Create system prompt
            system_prompt = self._create_system_prompt(category)
            
            # Add farmer context if available
            if farmer_context:
                context_info = f"\nFarmer Context: Location: {farmer_context.get('location', 'Not specified')}, Crop: {farmer_context.get('crop_type', 'Not specified')}"
                system_prompt += context_info
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Farmer's question: {query}")
            ]
            
            # Get response from Gemini
            logger.info(f"Processing query: {query[:50]}...")
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Calculate confidence and extract suggestions
            confidence = self._calculate_confidence(answer, query)
            suggestions = self._extract_suggestions(answer)
            
            return FarmerQueryResponse(
                answer=answer,
                confidence_score=confidence,
                category=category,
                suggestions=suggestions,
                sources=["Gemini AI", "Agricultural Knowledge Base"],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return FarmerQueryResponse(
                answer="I apologize, but I'm experiencing technical difficulties. Please try again or consult your local agricultural extension officer.",
                confidence_score=0.0,
                category=QueryCategory.GENERAL,
                suggestions=["Try rephrasing your question", "Contact local agricultural extension office"],
                sources=[],
                timestamp=datetime.now()
            )
    
    def test_connection(self) -> bool:
        """Test Gemini API connection"""
        try:
            test_response = self.llm.invoke([HumanMessage(content="Hello, test connection")])
            return bool(test_response.content)
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {e}")
            return False

# Global instance
gemini_service = GeminiService()