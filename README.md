# 🌾 AI-Based Farmer Query Support System
**SIH 2025 - Team Project**

An intelligent agricultural advisory system that helps farmers get instant answers to their farming queries using Google's Gemini AI API.

## 🚀 Features

- **Text-based Query Processing**: Ask farming questions in natural language
- **Smart Categorization**: Automatically categorizes queries (crop management, pest control, weather, etc.)
- **Multi-language Support**: Designed to support multiple Indian languages
- **Weather Integration**: Get weather information for farming decisions
- **Market Price Information**: Access crop pricing data
- **Voice Support** (Coming Soon): Ask questions using voice
- **Image Analysis** (Coming Soon): Upload images for pest/disease identification
- **Confidence Scoring**: AI provides confidence levels for recommendations

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI/LLM**: Google Gemini API via LangChain
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Voice Processing**: Whisper API (Planned)
- **Image Processing**: ResNet50 (Planned)
- **Frontend**: Flutter (Mobile App)

## 📁 Project Structure

```
sihproject/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── farmer_query.py    # Main API endpoints
│   │   └── health.py          # Health check endpoints
│   └── services/
│       ├── __init__.py
│       ├── gemini_service.py  # Gemini API integration
│       └── additional_services.py  # Weather & market services
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── start.bat                 # Windows startup script
├── start.sh                  # Unix startup script
└── README.md                 # This file
```

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd sihproject
```

### 2. Create Environment File

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
```

**Required Environment Variables:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_openweather_api_key_here  # Optional
DATABASE_URL=postgresql://username:password@localhost/farmer_db
```

### 3. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

### 4. Run the Application

**Windows:**
```bash
./start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Manual Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

### 5. Access the API

- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/v1/health`

## 📡 API Endpoints

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/ask` | Main farmer query endpoint |
| `GET` | `/api/v1/ask-simple` | Simple GET query for testing |
| `GET` | `/api/v1/weather` | Get weather information |
| `GET` | `/api/v1/market-price` | Get crop market prices |
| `GET` | `/api/v1/categories` | List available query categories |
| `GET` | `/api/v1/test-gemini` | Test Gemini API connection |

### Example Usage

**Simple Query:**
```bash
curl "http://localhost:8000/api/v1/ask-simple?query=How to increase tomato yield&location=Maharashtra"
```

**Full Query (POST):**
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "My tomato plants have yellow spots on leaves",
    "category": "pest_disease",
    "location": "Karnataka",
    "crop_type": "tomato",
    "farmer_id": "farmer123"
  }'
```

**Response Example:**
```json
{
  "answer": "Yellow spots on tomato leaves could indicate early blight disease...",
  "confidence_score": 0.85,
  "category": "pest_disease",
  "suggestions": [
    "Apply copper-based fungicide",
    "Remove affected leaves",
    "Improve air circulation"
  ],
  "sources": ["Gemini AI", "Agricultural Knowledge Base"],
  "timestamp": "2025-09-25T10:30:00"
}
```

## 🧪 Testing the API

### 1. Test Gemini Connection
```bash
curl http://localhost:8000/api/v1/test-gemini
```

### 2. Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### 3. Sample Farmer Queries
```bash
# Crop management
curl "http://localhost:8000/api/v1/ask-simple?query=When should I plant wheat in Punjab?"

# Pest control
curl "http://localhost:8000/api/v1/ask-simple?query=How to control aphids in cotton crop?"

# Weather advice
curl "http://localhost:8000/api/v1/ask-simple?query=Should I irrigate my crops before expected rain?"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `WEATHER_API_KEY` | OpenWeather API key | No | - |
| `DATABASE_URL` | Database connection string | No | SQLite |
| `HOST` | Server host | No | localhost |
| `PORT` | Server port | No | 8000 |
| `DEBUG` | Debug mode | No | True |

### Query Categories

The system automatically categorizes queries into:
- `crop_management` - Planting, harvesting, varieties
- `pest_disease` - Pest control, disease management
- `weather` - Weather-related advice
- `market_price` - Pricing and market information
- `soil_health` - Soil testing and nutrition
- `irrigation` - Water management
- `fertilizer` - Nutrient management
- `general` - General farming questions

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] **Voice Processing**: Integrate Whisper API for speech-to-text
- [ ] **Image Analysis**: ResNet50 for pest/disease identification
- [ ] **Multi-language**: Support for Hindi, Telugu, Tamil, etc.
- [ ] **Real Market Data**: Integration with eNAM API
- [ ] **Personalization**: Learning from farmer's query history

### Phase 3 Features
- [ ] **Mobile App**: Flutter frontend
- [ ] **Offline Support**: Cached responses for common queries
- [ ] **Expert Consultation**: Connect with agricultural experts
- [ ] **Weather Alerts**: Proactive farming alerts

## 🤝 Integration with Flutter

Your Flutter app can integrate with this API:

```dart
// Example Flutter integration
class FarmerQueryService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  static Future<Map<String, dynamic>> askQuery(String query) async {
    final response = await http.get(
      Uri.parse('$baseUrl/ask-simple?query=$query'),
    );
    return json.decode(response.body);
  }
}
```

## 📊 Monitoring & Logging

- All API requests are logged with timestamps
- Health checks available at `/api/v1/health`
- Gemini API connection status monitoring
- Error tracking with detailed error messages

## 🐛 Troubleshooting

### Common Issues

**1. Gemini API Key Error**
```
Error: Gemini API key not configured
Solution: Add GEMINI_API_KEY to your .env file
```

**2. Import Errors**
```
Error: Import "langchain_google_genai" could not be resolved
Solution: Install dependencies with pip install -r requirements.txt
```

**3. Database Connection Issues**
```
Error: Database connection failed
Solution: Check DATABASE_URL in .env file
```

### Debug Mode

Set `DEBUG=True` in `.env` for detailed logging and auto-reload during development.

## 👥 Team Members

**SIH 2025 Team - AI Farmer Query Support System**
- Your role: LLM API Integration (Gemini API)
- Tech Stack: FastAPI + LangChain + Gemini AI

## 📄 License

This project is developed for SIH 2025 competition.

---

**Ready to help farmers with AI! 🌾🤖**

For questions or issues, check the `/docs` endpoint or contact the development team.