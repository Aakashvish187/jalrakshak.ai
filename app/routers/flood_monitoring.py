"""
Flood Monitoring Router for JalRakshā AI

This module provides comprehensive flood monitoring and prediction capabilities
for all Indian cities with real-time risk assessment and emergency alerts.
"""

import logging
import sqlite3
import random
import time
import threading
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()

# Indian Cities Database with coordinates and flood risk factors
INDIAN_CITIES = {
    "Mumbai": {"state": "Maharashtra", "lat": 19.0760, "lng": 72.8777, "population": "20M", "flood_risk_factor": 0.8},
    "Delhi": {"state": "Delhi", "lat": 28.7041, "lng": 77.1025, "population": "19M", "flood_risk_factor": 0.3},
    "Bangalore": {"state": "Karnataka", "lat": 12.9716, "lng": 77.5946, "population": "12M", "flood_risk_factor": 0.4},
    "Chennai": {"state": "Tamil Nadu", "lat": 13.0827, "lng": 80.2707, "population": "11M", "flood_risk_factor": 0.9},
    "Kolkata": {"state": "West Bengal", "lat": 22.5726, "lng": 88.3639, "population": "15M", "flood_risk_factor": 0.85},
    "Hyderabad": {"state": "Telangana", "lat": 17.3850, "lng": 78.4867, "population": "10M", "flood_risk_factor": 0.5},
    "Pune": {"state": "Maharashtra", "lat": 18.5204, "lng": 73.8567, "population": "7M", "flood_risk_factor": 0.6},
    "Ahmedabad": {"state": "Gujarat", "lat": 23.0225, "lng": 72.5714, "population": "8M", "flood_risk_factor": 0.4},
    "Jaipur": {"state": "Rajasthan", "lat": 26.9124, "lng": 75.7873, "population": "4M", "flood_risk_factor": 0.2},
    "Surat": {"state": "Gujarat", "lat": 21.1702, "lng": 72.8311, "population": "6M", "flood_risk_factor": 0.7},
    "Lucknow": {"state": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462, "population": "4M", "flood_risk_factor": 0.5},
    "Kanpur": {"state": "Uttar Pradesh", "lat": 26.4499, "lng": 80.3319, "population": "3M", "flood_risk_factor": 0.6},
    "Nagpur": {"state": "Maharashtra", "lat": 21.1458, "lng": 79.0882, "population": "3M", "flood_risk_factor": 0.3},
    "Indore": {"state": "Madhya Pradesh", "lat": 22.7196, "lng": 75.8577, "population": "3M", "flood_risk_factor": 0.4},
    "Thane": {"state": "Maharashtra", "lat": 19.2183, "lng": 72.9781, "population": "2M", "flood_risk_factor": 0.8},
    "Bhopal": {"state": "Madhya Pradesh", "lat": 23.2599, "lng": 77.4126, "population": "2M", "flood_risk_factor": 0.3},
    "Visakhapatnam": {"state": "Andhra Pradesh", "lat": 17.6868, "lng": 83.2185, "population": "2M", "flood_risk_factor": 0.7},
    "Pimpri-Chinchwad": {"state": "Maharashtra", "lat": 18.6298, "lng": 73.7997, "population": "2M", "flood_risk_factor": 0.6},
    "Patna": {"state": "Bihar", "lat": 25.5941, "lng": 85.1376, "population": "2M", "flood_risk_factor": 0.8},
    "Vadodara": {"state": "Gujarat", "lat": 22.3072, "lng": 73.1812, "population": "2M", "flood_risk_factor": 0.5},
    "Kochi": {"state": "Kerala", "lat": 9.9312, "lng": 76.2673, "population": "2M", "flood_risk_factor": 0.9},
    "Coimbatore": {"state": "Tamil Nadu", "lat": 11.0168, "lng": 76.9558, "population": "2M", "flood_risk_factor": 0.4},
    "Trivandrum": {"state": "Kerala", "lat": 8.5241, "lng": 76.9366, "population": "1M", "flood_risk_factor": 0.8},
    "Madurai": {"state": "Tamil Nadu", "lat": 9.9252, "lng": 78.1198, "population": "1M", "flood_risk_factor": 0.5},
    "Tiruchirappalli": {"state": "Tamil Nadu", "lat": 10.7905, "lng": 78.7047, "population": "1M", "flood_risk_factor": 0.6},
    "Salem": {"state": "Tamil Nadu", "lat": 11.6643, "lng": 78.1460, "population": "1M", "flood_risk_factor": 0.3},
    "Tirunelveli": {"state": "Tamil Nadu", "lat": 8.7139, "lng": 77.7567, "population": "1M", "flood_risk_factor": 0.4},
    "Erode": {"state": "Tamil Nadu", "lat": 11.3410, "lng": 77.7172, "population": "1M", "flood_risk_factor": 0.3},
    "Vellore": {"state": "Tamil Nadu", "lat": 12.9202, "lng": 79.1500, "population": "1M", "flood_risk_factor": 0.4},
    "Thanjavur": {"state": "Tamil Nadu", "lat": 10.7867, "lng": 79.1378, "population": "1M", "flood_risk_factor": 0.6},
    "Tiruppur": {"state": "Tamil Nadu", "lat": 11.1085, "lng": 77.3411, "population": "1M", "flood_risk_factor": 0.3},
    "Dindigul": {"state": "Tamil Nadu", "lat": 10.3529, "lng": 77.9755, "population": "1M", "flood_risk_factor": 0.4},
    "Thoothukudi": {"state": "Tamil Nadu", "lat": 8.7642, "lng": 78.1348, "population": "1M", "flood_risk_factor": 0.5},
    "Hosur": {"state": "Tamil Nadu", "lat": 12.7404, "lng": 77.8253, "population": "1M", "flood_risk_factor": 0.3},
    "Nagercoil": {"state": "Tamil Nadu", "lat": 8.1774, "lng": 77.4343, "population": "1M", "flood_risk_factor": 0.6},
    "Kanchipuram": {"state": "Tamil Nadu", "lat": 12.8338, "lng": 79.7000, "population": "1M", "flood_risk_factor": 0.4},
    "Cuddalore": {"state": "Tamil Nadu", "lat": 11.7488, "lng": 79.7714, "population": "1M", "flood_risk_factor": 0.8},
    "Kumbakonam": {"state": "Tamil Nadu", "lat": 10.9595, "lng": 79.3842, "population": "1M", "flood_risk_factor": 0.5},
    "Tiruvannamalai": {"state": "Tamil Nadu", "lat": 12.2319, "lng": 79.0676, "population": "1M", "flood_risk_factor": 0.3},
    "Pollachi": {"state": "Tamil Nadu", "lat": 10.6589, "lng": 77.0083, "population": "1M", "flood_risk_factor": 0.4},
    "Rajapalayam": {"state": "Tamil Nadu", "lat": 9.4529, "lng": 77.5534, "population": "1M", "flood_risk_factor": 0.3},
    "Gudiyatham": {"state": "Tamil Nadu", "lat": 12.9448, "lng": 78.8734, "population": "1M", "flood_risk_factor": 0.3},
    "Pudukkottai": {"state": "Tamil Nadu", "lat": 10.3811, "lng": 78.8211, "population": "1M", "flood_risk_factor": 0.4},
    "Vaniyambadi": {"state": "Tamil Nadu", "lat": 12.6869, "lng": 78.6203, "population": "1M", "flood_risk_factor": 0.3},
    "Ambur": {"state": "Tamil Nadu", "lat": 12.7917, "lng": 78.7167, "population": "1M", "flood_risk_factor": 0.3},
    "Nagapattinam": {"state": "Tamil Nadu", "lat": 10.7667, "lng": 79.8333, "population": "1M", "flood_risk_factor": 0.8},
    "Tirupathur": {"state": "Tamil Nadu", "lat": 12.5000, "lng": 78.5667, "population": "1M", "flood_risk_factor": 0.3},
    "Karaikudi": {"state": "Tamil Nadu", "lat": 10.0667, "lng": 78.7833, "population": "1M", "flood_risk_factor": 0.4},
    "Tiruvallur": {"state": "Tamil Nadu", "lat": 13.1333, "lng": 79.9000, "population": "1M", "flood_risk_factor": 0.4},
    "Ranipet": {"state": "Tamil Nadu", "lat": 12.9333, "lng": 79.3333, "population": "1M", "flood_risk_factor": 0.3},
    "Arcot": {"state": "Tamil Nadu", "lat": 12.9000, "lng": 79.3167, "population": "1M", "flood_risk_factor": 0.3},
    "Arakkonam": {"state": "Tamil Nadu", "lat": 13.0833, "lng": 79.6667, "population": "1M", "flood_risk_factor": 0.3},
    "Virudhunagar": {"state": "Tamil Nadu", "lat": 9.5833, "lng": 77.9667, "population": "1M", "flood_risk_factor": 0.3},
    "Sivakasi": {"state": "Tamil Nadu", "lat": 9.4500, "lng": 77.8167, "population": "1M", "flood_risk_factor": 0.3},
    "Tenkasi": {"state": "Tamil Nadu", "lat": 8.9667, "lng": 77.3167, "population": "1M", "flood_risk_factor": 0.4},
    "Palani": {"state": "Tamil Nadu", "lat": 10.4500, "lng": 77.5167, "population": "1M", "flood_risk_factor": 0.3},
    "Paramakudi": {"state": "Tamil Nadu", "lat": 9.5500, "lng": 78.5833, "population": "1M", "flood_risk_factor": 0.4},
    "Tiruchengode": {"state": "Tamil Nadu", "lat": 11.3833, "lng": 77.9000, "population": "1M", "flood_risk_factor": 0.3},
    "Karur": {"state": "Tamil Nadu", "lat": 10.9500, "lng": 78.0833, "population": "1M", "flood_risk_factor": 0.4},
    "Valparai": {"state": "Tamil Nadu", "lat": 10.3333, "lng": 76.9667, "population": "1M", "flood_risk_factor": 0.6},
    "Sankarankovil": {"state": "Tamil Nadu", "lat": 9.1667, "lng": 77.5500, "population": "1M", "flood_risk_factor": 0.3},
    "Tenkasi": {"state": "Tamil Nadu", "lat": 8.9667, "lng": 77.3167, "population": "1M", "flood_risk_factor": 0.4},
    "Cumbum": {"state": "Tamil Nadu", "lat": 9.7333, "lng": 77.2833, "population": "1M", "flood_risk_factor": 0.3},
    "Rajapalayam": {"state": "Tamil Nadu", "lat": 9.4529, "lng": 77.5534, "population": "1M", "flood_risk_factor": 0.3},
    "Sivaganga": {"state": "Tamil Nadu", "lat": 9.8667, "lng": 78.4833, "population": "1M", "flood_risk_factor": 0.4},
    "Kodungallur": {"state": "Kerala", "lat": 10.2167, "lng": 76.2000, "population": "1M", "flood_risk_factor": 0.8},
    "Kollam": {"state": "Kerala", "lat": 8.8806, "lng": 76.5917, "population": "1M", "flood_risk_factor": 0.7},
    "Thrissur": {"state": "Kerala", "lat": 10.5167, "lng": 76.2167, "population": "1M", "flood_risk_factor": 0.6},
    "Palakkad": {"state": "Kerala", "lat": 10.7667, "lng": 76.6500, "population": "1M", "flood_risk_factor": 0.5},
    "Malappuram": {"state": "Kerala", "lat": 11.0500, "lng": 76.0833, "population": "1M", "flood_risk_factor": 0.6},
    "Kozhikode": {"state": "Kerala", "lat": 11.2588, "lng": 75.7804, "population": "1M", "flood_risk_factor": 0.7},
    "Kannur": {"state": "Kerala", "lat": 11.8667, "lng": 75.3667, "population": "1M", "flood_risk_factor": 0.6},
    "Kasaragod": {"state": "Kerala", "lat": 12.5000, "lng": 75.0000, "population": "1M", "flood_risk_factor": 0.7},
    "Alappuzha": {"state": "Kerala", "lat": 9.5000, "lng": 76.3333, "population": "1M", "flood_risk_factor": 0.9},
    "Pathanamthitta": {"state": "Kerala", "lat": 9.2667, "lng": 76.7833, "population": "1M", "flood_risk_factor": 0.6},
    "Kottayam": {"state": "Kerala", "lat": 9.5833, "lng": 76.5167, "population": "1M", "flood_risk_factor": 0.7},
    "Idukki": {"state": "Kerala", "lat": 9.8500, "lng": 76.9667, "population": "1M", "flood_risk_factor": 0.8},
    "Ernakulam": {"state": "Kerala", "lat": 9.9667, "lng": 76.2833, "population": "1M", "flood_risk_factor": 0.8},
    "Wayanad": {"state": "Kerala", "lat": 11.6000, "lng": 76.0833, "population": "1M", "flood_risk_factor": 0.7},
    "Kasaragod": {"state": "Kerala", "lat": 12.5000, "lng": 75.0000, "population": "1M", "flood_risk_factor": 0.7},
    "Kannur": {"state": "Kerala", "lat": 11.8667, "lng": 75.3667, "population": "1M", "flood_risk_factor": 0.6},
    "Kozhikode": {"state": "Kerala", "lat": 11.2588, "lng": 75.7804, "population": "1M", "flood_risk_factor": 0.7},
    "Malappuram": {"state": "Kerala", "lat": 11.0500, "lng": 76.0833, "population": "1M", "flood_risk_factor": 0.6},
    "Palakkad": {"state": "Kerala", "lat": 10.7667, "lng": 76.6500, "population": "1M", "flood_risk_factor": 0.5},
    "Thrissur": {"state": "Kerala", "lat": 10.5167, "lng": 76.2167, "population": "1M", "flood_risk_factor": 0.6},
    "Kollam": {"state": "Kerala", "lat": 8.8806, "lng": 76.5917, "population": "1M", "flood_risk_factor": 0.7},
    "Kodungallur": {"state": "Kerala", "lat": 10.2167, "lng": 76.2000, "population": "1M", "flood_risk_factor": 0.8},
    "Alappuzha": {"state": "Kerala", "lat": 9.5000, "lng": 76.3333, "population": "1M", "flood_risk_factor": 0.9},
    "Pathanamthitta": {"state": "Kerala", "lat": 9.2667, "lng": 76.7833, "population": "1M", "flood_risk_factor": 0.6},
    "Kottayam": {"state": "Kerala", "lat": 9.5833, "lng": 76.5167, "population": "1M", "flood_risk_factor": 0.7},
    "Idukki": {"state": "Kerala", "lat": 9.8500, "lng": 76.9667, "population": "1M", "flood_risk_factor": 0.8},
    "Ernakulam": {"state": "Kerala", "lat": 9.9667, "lng": 76.2833, "population": "1M", "flood_risk_factor": 0.8},
    "Wayanad": {"state": "Kerala", "lat": 11.6000, "lng": 76.0833, "population": "1M", "flood_risk_factor": 0.7}
}

# Pydantic models
class FloodData(BaseModel):
    city: str
    water_level: int
    rainfall: int
    river_flow: int
    timestamp: Optional[datetime] = None

class FloodPrediction(BaseModel):
    city: str
    risk_level: str
    confidence: float
    water_level: int
    rainfall: int
    river_flow: int
    reason: str
    recommendation: str
    solutions: str
    helpline: str
    timestamp: datetime
    coordinates: Dict[str, float]
    population: str

class CityRiskStatus(BaseModel):
    city: str
    state: str
    risk_level: str
    confidence: float
    water_level: int
    rainfall: int
    river_flow: int
    population: str
    coordinates: Dict[str, float]
    last_updated: datetime

class FloodMonitoringResponse(BaseModel):
    cities: List[CityRiskStatus]
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    total_cities: int
    last_updated: datetime

# Global variables for real-time monitoring
flood_data_cache = {}
monitoring_active = False

def init_flood_database():
    """Initialize flood monitoring database."""
    conn = sqlite3.connect('flood_monitoring.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flood_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            state TEXT,
            water_level INTEGER,
            rainfall INTEGER,
            river_flow INTEGER,
            risk_level TEXT,
            confidence REAL,
            reason TEXT,
            recommendation TEXT,
            solutions TEXT,
            helpline TEXT,
            timestamp TEXT,
            coordinates TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_flood_data(city: str, flood_data: FloodData, prediction: FloodPrediction):
    """Save flood data to database."""
    conn = sqlite3.connect('flood_monitoring.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO flood_data (city, state, water_level, rainfall, river_flow, risk_level, 
                              confidence, reason, recommendation, solutions, helpline, timestamp, coordinates)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        city,
        INDIAN_CITIES[city]["state"],
        flood_data.water_level,
        flood_data.rainfall,
        flood_data.river_flow,
        prediction.risk_level,
        prediction.confidence,
        prediction.reason,
        prediction.recommendation,
        prediction.solutions,
        prediction.helpline,
        prediction.timestamp.isoformat(),
        f"{prediction.coordinates['lat']},{prediction.coordinates['lng']}"
    ))
    conn.commit()
    conn.close()

def generate_flood_data(city: str) -> FloodData:
    """Generate realistic flood data for a city."""
    city_info = INDIAN_CITIES[city]
    flood_risk_factor = city_info["flood_risk_factor"]
    
    # Generate data based on flood risk factor
    base_water_level = random.randint(0, 50)
    base_rainfall = random.randint(0, 100)
    base_river_flow = random.randint(0, 200)
    
    # Adjust based on flood risk factor
    water_level = min(100, int(base_water_level + (flood_risk_factor * 50)))
    rainfall = min(300, int(base_rainfall + (flood_risk_factor * 100)))
    river_flow = min(600, int(base_river_flow + (flood_risk_factor * 200)))
    
    return FloodData(
        city=city,
        water_level=water_level,
        rainfall=rainfall,
        river_flow=river_flow,
        timestamp=datetime.now()
    )

def predict_flood_risk(flood_data: FloodData) -> FloodPrediction:
    """Predict flood risk based on sensor data."""
    city_info = INDIAN_CITIES[flood_data.city]
    
    # Risk calculation with city-specific factors
    risk_score = (
        (flood_data.water_level / 100) * 0.4 +
        (flood_data.rainfall / 300) * 0.3 +
        (flood_data.river_flow / 600) * 0.3
    ) * city_info["flood_risk_factor"]
    
    # Determine risk level
    if risk_score > 0.7:
        risk_level = "HIGH"
        confidence = min(95, 70 + (risk_score * 25))
        reason = "Severe flood conditions detected with high water levels and heavy rainfall"
        recommendation = "🚨 IMMEDIATE EVACUATION REQUIRED - Activate emergency protocols"
        solutions = (
            "1. 🚨 Evacuate to higher ground immediately\n"
            "2. 📞 Call emergency helplines: 1078, 011-26701728\n"
            "3. 📱 Keep mobile phones charged and ready\n"
            "4. 🚫 Do NOT cross flooded roads or bridges\n"
            "5. 🏠 Move essential documents and medicines to safe place\n"
            "6. 🚁 Authorities must deploy rescue boats and helicopters\n"
            "7. 📢 Broadcast emergency alerts to all residents"
        )
        helpline = (
            "🚨 EMERGENCY HELPLINES:\n"
            "• National Disaster Helpline: 1078\n"
            "• NDMA Helpline: 011-26701728\n"
            "• State Disaster Control: 1070\n"
            "• Animal Rescue: 1962\n"
            "• Police: 100\n"
            "• Fire Service: 101\n"
            "• Ambulance: 108"
        )
    elif risk_score > 0.4:
        risk_level = "MEDIUM"
        confidence = min(85, 50 + (risk_score * 35))
        reason = "Moderate flood risk with rising water levels and increasing rainfall"
        recommendation = "⚠️ STAY PREPARED - Monitor situation closely and be ready to evacuate"
        solutions = (
            "1. 📦 Pack essential items and documents\n"
            "2. 📱 Monitor weather alerts and government updates\n"
            "3. 👥 Ensure elderly and children have support\n"
            "4. 🚫 Avoid unnecessary travel\n"
            "5. 🏠 Check drainage systems and clear blockages\n"
            "6. 📢 Local authorities should prepare emergency shelters\n"
            "7. 💧 Store drinking water and food supplies"
        )
        helpline = (
            "📞 PREPARATION HELPLINES:\n"
            "• State Disaster Helpline: 1070\n"
            "• Weather Updates: 1800-180-1717\n"
            "• Animal Rescue: 1962\n"
            "• Local Administration: Check local numbers"
        )
    else:
        risk_level = "LOW"
        confidence = min(75, 30 + (risk_score * 45))
        reason = "Normal conditions with safe water levels"
        recommendation = "✅ SITUATION NORMAL - Continue monitoring and stay informed"
        solutions = (
            "1. 📅 Continue normal daily routine\n"
            "2. 📰 Stay informed about weather forecasts\n"
            "3. 🏘️ Educate community about flood safety\n"
            "4. 🚰 Ensure drainage systems are clear\n"
            "5. 📱 Keep emergency contacts updated\n"
            "6. 🏠 Authorities should maintain monitoring systems\n"
            "7. 📚 Review emergency preparedness plans"
        )
        helpline = (
            "📞 GENERAL HELPLINES:\n"
            "• General Emergency: 112\n"
            "• Weather Information: 1800-180-1717\n"
            "• Local Administration: Check local numbers"
        )
    
    return FloodPrediction(
        city=flood_data.city,
        risk_level=risk_level,
        confidence=confidence,
        water_level=flood_data.water_level,
        rainfall=flood_data.rainfall,
        river_flow=flood_data.river_flow,
        reason=reason,
        recommendation=recommendation,
        solutions=solutions,
        helpline=helpline,
        timestamp=datetime.now(),
        coordinates={"lat": city_info["lat"], "lng": city_info["lng"]},
        population=city_info["population"]
    )

def start_flood_monitoring():
    """Start real-time flood monitoring for all cities."""
    global monitoring_active, flood_data_cache
    monitoring_active = True
    
    def monitor_cities():
        while monitoring_active:
            for city in INDIAN_CITIES.keys():
                try:
                    # Generate flood data
                    flood_data = generate_flood_data(city)
                    
                    # Predict flood risk
                    prediction = predict_flood_risk(flood_data)
                    
                    # Save to database
                    save_flood_data(city, flood_data, prediction)
                    
                    # Update cache
                    flood_data_cache[city] = {
                        "city": city,
                        "state": INDIAN_CITIES[city]["state"],
                        "risk_level": prediction.risk_level,
                        "confidence": prediction.confidence,
                        "water_level": prediction.water_level,
                        "rainfall": prediction.rainfall,
                        "river_flow": prediction.river_flow,
                        "population": prediction.population,
                        "coordinates": prediction.coordinates,
                        "last_updated": prediction.timestamp
                    }
                    
                except Exception as e:
                    logger.error(f"Error monitoring {city}: {e}")
            
            # Wait before next update
            time.sleep(30)  # Update every 30 seconds
    
    # Start monitoring in background thread
    monitoring_thread = threading.Thread(target=monitor_cities, daemon=True)
    monitoring_thread.start()
    logger.info("Flood monitoring started for all Indian cities")

def stop_flood_monitoring():
    """Stop flood monitoring."""
    global monitoring_active
    monitoring_active = False
    logger.info("Flood monitoring stopped")

@router.post("/flood/predict", response_model=FloodPrediction)
async def predict_flood(flood_data: FloodData):
    """
    Predict flood risk for a specific city.
    
    Args:
        flood_data: Sensor data for flood prediction
        
    Returns:
        FloodPrediction: Risk assessment and recommendations
    """
    try:
        if flood_data.city not in INDIAN_CITIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City '{flood_data.city}' not found in database"
            )
        
        # Generate prediction
        prediction = predict_flood_risk(flood_data)
        
        # Save to database
        save_flood_data(flood_data.city, flood_data, prediction)
        
        logger.info(f"Flood prediction generated for {flood_data.city}: {prediction.risk_level}")
        return prediction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to predict flood risk: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict flood risk: {str(e)}"
        )

@router.get("/flood/monitoring", response_model=FloodMonitoringResponse)
async def get_flood_monitoring():
    """
    Get real-time flood monitoring data for all cities.
    
    Returns:
        FloodMonitoringResponse: Current flood status for all cities
    """
    try:
        if not flood_data_cache:
            # Start monitoring if not active
            start_flood_monitoring()
            time.sleep(5)  # Wait for initial data
        
        cities = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for city_data in flood_data_cache.values():
            cities.append(CityRiskStatus(**city_data))
            
            if city_data["risk_level"] == "HIGH":
                high_risk_count += 1
            elif city_data["risk_level"] == "MEDIUM":
                medium_risk_count += 1
            else:
                low_risk_count += 1
        
        response = FloodMonitoringResponse(
            cities=cities,
            high_risk_count=high_risk_count,
            medium_risk_count=medium_risk_count,
            low_risk_count=low_risk_count,
            total_cities=len(cities),
            last_updated=datetime.now()
        )
        
        logger.info(f"Flood monitoring data retrieved: {high_risk_count} high risk, {medium_risk_count} medium risk, {low_risk_count} low risk")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get flood monitoring data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flood monitoring data: {str(e)}"
        )

@router.get("/flood/cities")
async def get_cities():
    """
    Get list of all monitored cities with their information.
    
    Returns:
        dict: List of cities with coordinates and risk factors
    """
    try:
        cities = []
        for city, info in INDIAN_CITIES.items():
            cities.append({
                "name": city,
                "state": info["state"],
                "coordinates": {"lat": info["lat"], "lng": info["lng"]},
                "population": info["population"],
                "flood_risk_factor": info["flood_risk_factor"]
            })
        
        return {
            "cities": cities,
            "total_cities": len(cities),
            "states": list(set(info["state"] for info in INDIAN_CITIES.values()))
        }
        
    except Exception as e:
        logger.error(f"Failed to get cities list: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cities list: {str(e)}"
        )

@router.get("/flood/history/{city}")
async def get_city_flood_history(city: str, limit: int = 50):
    """
    Get flood history for a specific city.
    
    Args:
        city: City name
        limit: Number of records to return
        
    Returns:
        list: Historical flood data for the city
    """
    try:
        if city not in INDIAN_CITIES:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{city}' not found"
            )
        
        conn = sqlite3.connect('flood_monitoring.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT city, water_level, rainfall, river_flow, risk_level, confidence, 
                   reason, recommendation, solutions, helpline, timestamp, coordinates
            FROM flood_data 
            WHERE city = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (city, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "city": row[0],
                "water_level": row[1],
                "rainfall": row[2],
                "river_flow": row[3],
                "risk_level": row[4],
                "confidence": row[5],
                "reason": row[6],
                "recommendation": row[7],
                "solutions": row[8],
                "helpline": row[9],
                "timestamp": row[10],
                "coordinates": row[11]
            })
        
        return {
            "city": city,
            "history": history,
            "count": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get flood history for {city}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flood history: {str(e)}"
        )

@router.post("/flood/monitoring/start")
async def start_monitoring():
    """
    Start real-time flood monitoring.
    
    Returns:
        dict: Success message
    """
    try:
        start_flood_monitoring()
        return {
            "message": "Flood monitoring started successfully",
            "cities_monitored": len(INDIAN_CITIES),
            "update_interval": "30 seconds"
        }
    except Exception as e:
        logger.error(f"Failed to start flood monitoring: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start flood monitoring: {str(e)}"
        )

@router.post("/flood/monitoring/stop")
async def stop_monitoring():
    """
    Stop real-time flood monitoring.
    
    Returns:
        dict: Success message
    """
    try:
        stop_flood_monitoring()
        return {"message": "Flood monitoring stopped successfully"}
    except Exception as e:
        logger.error(f"Failed to stop flood monitoring: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop flood monitoring: {str(e)}"
        )

@router.get("/flood/stats")
async def get_flood_stats():
    """
    Get flood monitoring statistics.
    
    Returns:
        dict: Statistics about flood monitoring
    """
    try:
        conn = sqlite3.connect('flood_monitoring.db')
        cursor = conn.cursor()
        
        # Get total records
        cursor.execute("SELECT COUNT(*) FROM flood_data")
        total_records = cursor.fetchone()[0]
        
        # Get records by risk level
        cursor.execute("SELECT risk_level, COUNT(*) FROM flood_data GROUP BY risk_level")
        risk_stats = dict(cursor.fetchall())
        
        # Get recent high-risk alerts
        cursor.execute("""
            SELECT city, risk_level, timestamp 
            FROM flood_data 
            WHERE risk_level = 'HIGH' 
            ORDER BY timestamp DESC 
            LIMIT 10
        """)
        recent_alerts = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_records": total_records,
            "risk_distribution": risk_stats,
            "recent_high_risk_alerts": [
                {"city": row[0], "risk_level": row[1], "timestamp": row[2]}
                for row in recent_alerts
            ],
            "monitoring_active": monitoring_active,
            "cities_monitored": len(INDIAN_CITIES)
        }
        
    except Exception as e:
        logger.error(f"Failed to get flood stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flood stats: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint for flood monitoring service.
    
    Returns:
        dict: Health status and monitoring information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JalRaksha AI Flood Monitoring",
        "monitoring_active": monitoring_active,
        "cities_monitored": len(INDIAN_CITIES),
        "cache_size": len(flood_data_cache)
    }

# Initialize database and start monitoring on module load
init_flood_database()
start_flood_monitoring()
