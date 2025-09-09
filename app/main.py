"""
JalRakshā AI - Flood & Disaster Early Warning & Rescue Management System
FastAPI Main Application Entry Point

This module serves as the main entry point for the FastAPI application,
handling CORS, middleware, and route registration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.routers import predict, alerts, sos, flood_monitoring, disaster, iot_enhanced
from app.ml_model import initialize_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    Initializes database and loads ML model on startup.
    """
    # Startup
    logger.info("Starting JalRakshā AI application...")
    await init_db()
    logger.info("Database initialized successfully")
    
    # Initialize ML model
    logger.info("Initializing ML model...")
    if initialize_model():
        logger.info("ML model initialized successfully")
    else:
        logger.error("Failed to initialize ML model")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down JalRakshā AI application...")


# Create FastAPI application instance
app = FastAPI(
    title="JalRakshā AI - Flood Prediction System",
    description="AI-powered flood and disaster early warning system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/api/v1", tags=["predictions"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(sos.router, prefix="/api/v1", tags=["sos"])
app.include_router(flood_monitoring.router, prefix="/api/v1", tags=["flood-monitoring"])
app.include_router(disaster.router, prefix="/api", tags=["disaster"])
app.include_router(iot_enhanced.router, prefix="/api/v1", tags=["iot"])


@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "message": "Welcome to JalRakshā AI - Flood Prediction System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Returns the current status of the application.
    """
    return {"status": "ok", "service": "JalRakshā AI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
