"""
Prediction Router for Flood Risk Assessment

This module contains the API endpoints for flood risk prediction,
including the main prediction endpoint and related functionality.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PredictionRequest, PredictionResponse
from app.crud import AlertCRUD
from app.ml_model import predict_flood_risk, predictor

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_flood_risk_endpoint(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict flood risk level based on environmental parameters.
    
    This endpoint accepts water level, rainfall, and river flow measurements
    and returns a flood risk prediction with confidence score.
    
    Args:
        request: Prediction request containing environmental parameters
        db: Database session dependency
        
    Returns:
        PredictionResponse: Risk level, confidence, and timestamp
        
    Raises:
        HTTPException: If prediction fails or model is not available
    """
    try:
        logger.info(f"Received prediction request: water_level={request.water_level}, "
                   f"rainfall={request.rainfall}, river_flow={request.river_flow}")
        
        # Check if model is trained
        if not predictor.is_trained:
            logger.error("ML model is not trained")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model is not available. Please try again later."
            )
        
        # Make prediction
        risk_level, confidence = predict_flood_risk(
            water_level=request.water_level,
            rainfall=request.rainfall,
            river_flow=request.river_flow
        )
        
        # Create timestamp
        timestamp = datetime.utcnow()
        
        # Save prediction to database
        try:
            alert = AlertCRUD.create_alert(
                db=db,
                water_level=request.water_level,
                rainfall=request.rainfall,
                river_flow=request.river_flow,
                risk_level=risk_level,
                confidence=confidence,
                timestamp=timestamp
            )
            logger.info(f"Prediction saved to database with ID {alert.id}")
        except Exception as e:
            logger.error(f"Failed to save prediction to database: {e}")
            # Continue with response even if database save fails
        
        # Prepare response
        response = PredictionResponse(
            risk_level=risk_level,
            confidence=round(confidence, 3),
            timestamp=timestamp
        )
        
        logger.info(f"Prediction completed: {risk_level} (confidence: {confidence:.3f})")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/model-info")
async def get_model_info():
    """
    Get information about the current ML model.
    
    Returns:
        dict: Model information including status, type, and configuration
    """
    try:
        model_info = predictor.get_model_info()
        logger.info("Model info requested")
        return model_info
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )


@router.post("/retrain")
async def retrain_model():
    """
    Retrain the ML model with fresh synthetic data.
    
    This endpoint allows for model retraining, which can be useful
    for updating the model with new patterns or improving performance.
    
    Returns:
        dict: Training results and metrics
    """
    try:
        logger.info("Model retraining requested")
        
        # Retrain the model
        success = predictor.train_and_save()
        
        if success:
            model_info = predictor.get_model_info()
            logger.info("Model retraining completed successfully")
            return {
                "status": "success",
                "message": "Model retrained successfully",
                "model_info": model_info
            }
        else:
            logger.error("Model retraining failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model retraining failed"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model retraining failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model retraining failed: {str(e)}"
        )
