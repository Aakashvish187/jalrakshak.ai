"""
Database Configuration and Connection Management

This module handles SQLite database setup, connection management,
and provides database session dependency for FastAPI.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from app.models import Base

logger = logging.getLogger(__name__)

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./jalraksha_ai.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    This function provides a database session for FastAPI endpoints
    and ensures proper session cleanup after use.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    
    Provides a database session with automatic cleanup.
    Useful for non-FastAPI contexts like ML model training.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database context error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def init_db():
    """
    Initialize the database by creating all tables.
    
    This function creates all database tables defined in the models.
    It's called during application startup.
    """
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with get_db_context() as db:
            # Simple query to test connection
            db.execute("SELECT 1")
        logger.info("Database connection check successful")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


def get_db_stats() -> dict:
    """
    Get basic database statistics.
    
    Returns:
        dict: Database statistics including table counts
    """
    try:
        with get_db_context() as db:
            # Get alerts count
            alerts_count = db.execute("SELECT COUNT(*) FROM alerts").scalar()
            
            return {
                "total_alerts": alerts_count,
                "database_url": SQLALCHEMY_DATABASE_URL,
                "status": "connected"
            }
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {
            "total_alerts": 0,
            "database_url": SQLALCHEMY_DATABASE_URL,
            "status": "error",
            "error": str(e)
        }
