"""
FastAPI Main Application
Our Voice, Our Rights - MGNREGA Transparency Dashboard
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import get_settings
from .database import engine, Base
from .routers import districts, geolocate

# Create database tables
Base.metadata.create_all(bind=engine)

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Our Voice, Our Rights - MGNREGA Dashboard API",
    description="Digital India Initiative - MGNREGA Transparency Dashboard API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = settings.cors_origins if not settings.debug else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(districts.router, prefix="/api/v1")
app.include_router(geolocate.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Our Voice, Our Rights - MGNREGA Dashboard API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting MGNREGA Dashboard API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down MGNREGA Dashboard API...")

