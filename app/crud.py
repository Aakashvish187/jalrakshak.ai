"""
CRUD Operations for Database Management

This module contains all database operations (Create, Read, Update, Delete)
for the JalRakshā AI application using SQLAlchemy ORM.
"""

import logging
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Alert

logger = logging.getLogger(__name__)


class AlertCRUD:
    """
    CRUD operations for Alert model.
    
    This class provides methods for creating, reading, and managing
    flood prediction alerts in the database.
    """
    
    @staticmethod
    def create_alert(
        db: Session,
        water_level: float,
        rainfall: float,
        river_flow: float,
        risk_level: str,
        confidence: float,
        timestamp: Optional[datetime] = None
    ) -> Alert:
        """
        Create a new flood prediction alert in the database.
        
        Args:
            db: Database session
            water_level: Water level measurement in meters
            rainfall: Rainfall measurement in millimeters
            river_flow: River flow rate in cubic meters per second
            risk_level: Predicted risk level (LOW, MEDIUM, HIGH)
            confidence: Model confidence score (0.0 to 1.0)
            timestamp: When the prediction was made (defaults to now)
            
        Returns:
            Alert: The created alert object
            
        Raises:
            Exception: If database operation fails
        """
        try:
            if timestamp is None:
                timestamp = datetime.utcnow()
                
            alert = Alert(
                water_level=water_level,
                rainfall=rainfall,
                river_flow=river_flow,
                risk_level=risk_level,
                confidence=confidence,
                timestamp=timestamp
            )
            
            db.add(alert)
            db.commit()
            db.refresh(alert)
            
            logger.info(f"Created alert with ID {alert.id} - Risk: {risk_level}")
            return alert
            
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_alert_by_id(db: Session, alert_id: int) -> Optional[Alert]:
        """
        Retrieve a specific alert by its ID.
        
        Args:
            db: Database session
            alert_id: Alert identifier
            
        Returns:
            Optional[Alert]: The alert if found, None otherwise
        """
        try:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                logger.info(f"Retrieved alert ID {alert_id}")
            else:
                logger.warning(f"Alert ID {alert_id} not found")
            return alert
        except Exception as e:
            logger.error(f"Failed to get alert by ID {alert_id}: {e}")
            raise
    
    @staticmethod
    def get_recent_alerts(db: Session, limit: int = 10) -> List[Alert]:
        """
        Retrieve the most recent alerts from the database.
        
        Args:
            db: Database session
            limit: Maximum number of alerts to return (default: 10)
            
        Returns:
            List[Alert]: List of recent alerts ordered by timestamp (newest first)
        """
        try:
            alerts = (
                db.query(Alert)
                .order_by(desc(Alert.timestamp))
                .limit(limit)
                .all()
            )
            
            logger.info(f"Retrieved {len(alerts)} recent alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get recent alerts: {e}")
            raise
    
    @staticmethod
    def get_alerts_by_risk_level(db: Session, risk_level: str) -> List[Alert]:
        """
        Retrieve alerts filtered by risk level.
        
        Args:
            db: Database session
            risk_level: Risk level to filter by (LOW, MEDIUM, HIGH)
            
        Returns:
            List[Alert]: List of alerts with the specified risk level
        """
        try:
            alerts = (
                db.query(Alert)
                .filter(Alert.risk_level == risk_level.upper())
                .order_by(desc(Alert.timestamp))
                .all()
            )
            
            logger.info(f"Retrieved {len(alerts)} alerts with risk level {risk_level}")
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts by risk level {risk_level}: {e}")
            raise
    
    @staticmethod
    def get_alerts_count(db: Session) -> int:
        """
        Get the total number of alerts in the database.
        
        Args:
            db: Database session
            
        Returns:
            int: Total number of alerts
        """
        try:
            count = db.query(Alert).count()
            logger.info(f"Total alerts count: {count}")
            return count
        except Exception as e:
            logger.error(f"Failed to get alerts count: {e}")
            raise
    
    @staticmethod
    def get_high_risk_alerts_count(db: Session) -> int:
        """
        Get the count of high-risk alerts.
        
        Args:
            db: Database session
            
        Returns:
            int: Number of high-risk alerts
        """
        try:
            count = db.query(Alert).filter(Alert.risk_level == "HIGH").count()
            logger.info(f"High-risk alerts count: {count}")
            return count
        except Exception as e:
            logger.error(f"Failed to get high-risk alerts count: {e}")
            raise
    
    @staticmethod
    def delete_alert(db: Session, alert_id: int) -> bool:
        """
        Delete an alert by its ID.
        
        Args:
            db: Database session
            alert_id: Alert identifier
            
        Returns:
            bool: True if deleted successfully, False if not found
        """
        try:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                db.delete(alert)
                db.commit()
                logger.info(f"Deleted alert ID {alert_id}")
                return True
            else:
                logger.warning(f"Alert ID {alert_id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Failed to delete alert ID {alert_id}: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def get_alerts_in_time_range(
        db: Session, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[Alert]:
        """
        Retrieve alerts within a specific time range.
        
        Args:
            db: Database session
            start_time: Start of time range
            end_time: End of time range
            
        Returns:
            List[Alert]: List of alerts within the time range
        """
        try:
            alerts = (
                db.query(Alert)
                .filter(Alert.timestamp >= start_time)
                .filter(Alert.timestamp <= end_time)
                .order_by(desc(Alert.timestamp))
                .all()
            )
            
            logger.info(f"Retrieved {len(alerts)} alerts in time range")
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts in time range: {e}")
            raise
