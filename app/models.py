"""
Pydantic Models and Database Schemas for JalRakshā AI

This module contains all the Pydantic models for request/response validation
and SQLAlchemy database models for data persistence.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./jalraksha_ai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class Alert(Base):
    """
    SQLAlchemy model for storing flood prediction alerts in the database.
    
    Attributes:
        id: Primary key identifier
        water_level: Water level measurement (meters)
        rainfall: Rainfall measurement (mm)
        river_flow: River flow rate (cubic meters per second)
        risk_level: Predicted risk level (LOW, MEDIUM, HIGH)
        confidence: Model confidence score (0.0 to 1.0)
        timestamp: When the prediction was made
    """
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    water_level = Column(Float, nullable=False, comment="Water level in meters")
    rainfall = Column(Float, nullable=False, comment="Rainfall in mm")
    river_flow = Column(Float, nullable=False, comment="River flow in cubic meters per second")
    risk_level = Column(String(10), nullable=False, comment="Risk level: LOW, MEDIUM, HIGH")
    confidence = Column(Float, nullable=False, comment="Model confidence score")
    timestamp = Column(DateTime, default=datetime.utcnow, comment="Prediction timestamp")


# Pydantic Models for API
class PredictionRequest(BaseModel):
    """
    Request model for flood prediction endpoint.
    
    Attributes:
        water_level: Water level measurement in meters
        rainfall: Rainfall measurement in millimeters
        river_flow: River flow rate in cubic meters per second
    """
    water_level: float = Field(
        ..., 
        ge=0.0, 
        le=50.0, 
        description="Water level in meters (0-50m)",
        example=2.5
    )
    rainfall: float = Field(
        ..., 
        ge=0.0, 
        le=500.0, 
        description="Rainfall in millimeters (0-500mm)",
        example=45.2
    )
    river_flow: float = Field(
        ..., 
        ge=0.0, 
        le=10000.0, 
        description="River flow in cubic meters per second (0-10000 m³/s)",
        example=150.8
    )

    class Config:
        schema_extra = {
            "example": {
                "water_level": 2.5,
                "rainfall": 45.2,
                "river_flow": 150.8
            }
        }


class PredictionResponse(BaseModel):
    """
    Response model for flood prediction endpoint.
    
    Attributes:
        risk_level: Predicted risk level (LOW, MEDIUM, HIGH)
        confidence: Model confidence score (0.0 to 1.0)
        timestamp: When the prediction was made
    """
    risk_level: str = Field(..., description="Predicted risk level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")
    timestamp: datetime = Field(..., description="Prediction timestamp")

    class Config:
        schema_extra = {
            "example": {
                "risk_level": "HIGH",
                "confidence": 0.87,
                "timestamp": "2025-01-06T14:30:12"
            }
        }


class AlertResponse(BaseModel):
    """
    Response model for individual alert data.
    
    Attributes:
        id: Alert identifier
        water_level: Water level measurement
        rainfall: Rainfall measurement
        river_flow: River flow rate
        risk_level: Predicted risk level
        confidence: Model confidence score
        timestamp: When the prediction was made
    """
    id: int
    water_level: float
    rainfall: float
    river_flow: float
    risk_level: str
    confidence: float
    timestamp: datetime

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "water_level": 2.5,
                "rainfall": 45.2,
                "river_flow": 150.8,
                "risk_level": "HIGH",
                "confidence": 0.87,
                "timestamp": "2025-01-06T14:30:12"
            }
        }


class AlertsResponse(BaseModel):
    """
    Response model for alerts list endpoint.
    
    Attributes:
        alerts: List of recent alerts
        count: Number of alerts returned
    """
    alerts: List[AlertResponse]
    count: int = Field(..., description="Number of alerts returned")

    class Config:
        schema_extra = {
            "example": {
                "alerts": [
                    {
                        "id": 1,
                        "water_level": 2.5,
                        "rainfall": 45.2,
                        "river_flow": 150.8,
                        "risk_level": "HIGH",
                        "confidence": 0.87,
                        "timestamp": "2025-01-06T14:30:12"
                    }
                ],
                "count": 1
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status: Service status
        service: Service name
    """
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")

    class Config:
        schema_extra = {
            "example": {
                "status": "ok",
                "service": "JalRakshā AI"
            }
        }
