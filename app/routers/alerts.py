"""
Alerts Router for Flood Prediction History

This module contains the API endpoints for retrieving and managing
flood prediction alerts and historical data.
"""

import logging
import sqlite3
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AlertsResponse, AlertResponse
from app.crud import AlertCRUD

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()


@router.get("/alerts", response_model=AlertsResponse)
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=100, description="Number of alerts to return"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (LOW, MEDIUM, HIGH)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve recent flood prediction alerts from the database.
    
    This endpoint returns the most recent alerts, optionally filtered by risk level.
    The alerts are ordered by timestamp with the newest first.
    
    Args:
        limit: Maximum number of alerts to return (1-100, default: 10)
        risk_level: Optional filter by risk level (LOW, MEDIUM, HIGH)
        db: Database session dependency
        
    Returns:
        AlertsResponse: List of alerts and count
        
    Raises:
        HTTPException: If database query fails
    """
    try:
        logger.info(f"Retrieving alerts: limit={limit}, risk_level={risk_level}")
        
        # Get alerts based on filters
        if risk_level:
            # Validate risk level
            if risk_level.upper() not in ["LOW", "MEDIUM", "HIGH"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid risk level. Must be LOW, MEDIUM, or HIGH"
                )
            
            alerts = AlertCRUD.get_alerts_by_risk_level(db, risk_level.upper())
            # Limit results after filtering
            alerts = alerts[:limit]
        else:
            alerts = AlertCRUD.get_recent_alerts(db, limit)
        
        # Convert to response format
        alert_responses = [
            AlertResponse(
                id=alert.id,
                water_level=alert.water_level,
                rainfall=alert.rainfall,
                river_flow=alert.river_flow,
                risk_level=alert.risk_level,
                confidence=alert.confidence,
                timestamp=alert.timestamp
            )
            for alert in alerts
        ]
        
        response = AlertsResponse(
            alerts=alert_responses,
            count=len(alert_responses)
        )
        
        logger.info(f"Retrieved {len(alert_responses)} alerts")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve alerts: {str(e)}"
        )


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert_by_id(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific alert by its ID.
    
    Args:
        alert_id: Alert identifier
        db: Database session dependency
        
    Returns:
        AlertResponse: The requested alert
        
    Raises:
        HTTPException: If alert not found or database error
    """
    try:
        logger.info(f"Retrieving alert with ID {alert_id}")
        
        alert = AlertCRUD.get_alert_by_id(db, alert_id)
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert with ID {alert_id} not found"
            )
        
        response = AlertResponse(
            id=alert.id,
            water_level=alert.water_level,
            rainfall=alert.rainfall,
            river_flow=alert.river_flow,
            risk_level=alert.risk_level,
            confidence=alert.confidence,
            timestamp=alert.timestamp
        )
        
        logger.info(f"Retrieved alert ID {alert_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve alert ID {alert_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve alert: {str(e)}"
        )


@router.get("/alerts/stats/summary")
async def get_alerts_summary(db: Session = Depends(get_db)):
    """
    Get summary statistics for all alerts.
    
    Returns:
        dict: Summary statistics including total counts and risk level distribution
    """
    try:
        logger.info("Retrieving alerts summary statistics")
        
        # Get total count
        total_alerts = AlertCRUD.get_alerts_count(db)
        
        # Get high-risk count
        high_risk_count = AlertCRUD.get_high_risk_alerts_count(db)
        
        # Get recent alerts for risk level distribution
        recent_alerts = AlertCRUD.get_recent_alerts(db, 100)  # Last 100 alerts
        
        # Calculate risk level distribution
        risk_distribution = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for alert in recent_alerts:
            risk_distribution[alert.risk_level] += 1
        
        summary = {
            "total_alerts": total_alerts,
            "high_risk_alerts": high_risk_count,
            "recent_alerts_analyzed": len(recent_alerts),
            "risk_distribution": risk_distribution,
            "high_risk_percentage": round((high_risk_count / total_alerts * 100), 2) if total_alerts > 0 else 0
        }
        
        logger.info(f"Retrieved alerts summary: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Failed to retrieve alerts summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve alerts summary: {str(e)}"
        )


@router.delete("/alerts/{alert_id}")
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific alert by its ID.
    
    Args:
        alert_id: Alert identifier
        db: Database session dependency
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If alert not found or deletion fails
    """
    try:
        logger.info(f"Deleting alert with ID {alert_id}")
        
        success = AlertCRUD.delete_alert(db, alert_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert with ID {alert_id} not found"
            )
        
        logger.info(f"Alert ID {alert_id} deleted successfully")
        return {"message": f"Alert with ID {alert_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete alert ID {alert_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete alert: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the alerts service.
    
    Returns:
        dict: Health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JalRaksha AI Alerts API"
    }


@router.get("/telegram-sos")
async def get_telegram_sos():
    """
    Get SOS requests from Telegram bot database.
    
    Returns:
        list: SOS requests from Telegram bot
    """
    try:
        conn = sqlite3.connect('telegram_sos.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, username, chat_id, message, location, status, timestamp
            FROM sos_requests 
            ORDER BY timestamp DESC
        ''')
        
        requests = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': req[0],
                'user_id': req[1],
                'username': req[2],
                'chat_id': req[3],
                'message': req[4],
                'location': req[5],
                'status': req[6],
                'timestamp': req[7]
            }
            for req in requests
        ]
    except Exception as e:
        logger.error(f"Failed to get Telegram SOS requests: {e}")
        return {"error": f"Database error: {str(e)}"}
