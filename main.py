import os
import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Import our modules
from app.routers import farmer_query, health
from app.config import get_settings
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting AI Farmer Query Support System...")
    await init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down application...")

# Create FastAPI app
app = FastAPI(
    title="AI-Based Farmer Query Support System",
    description="SIH 2025 - AI-powered advisory system for farmers using Gemini API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(farmer_query.router, prefix="/api/v1", tags=["Farmer Queries"])
app.include_router(health.router, prefix="/api/v1", tags=["Health Check"])

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to AI-Based Farmer Query Support System",
        "version": "1.0.0",
        "team": "SIH 2025",
        "status": "active"
    }

if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )