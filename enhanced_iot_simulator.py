#!/usr/bin/env python3
"""
Enhanced IoT Flood Monitoring Simulator for JalRakshā AI

This simulator generates realistic flood data for all Indian cities
and sends it to the FastAPI backend for real-time monitoring.
"""

import random
import time
import requests
import threading
import sqlite3
from datetime import datetime
import pytz
import json
from typing import Dict, List

# ---------------------------
# Configuration
# ---------------------------
FASTAPI_URL = "http://localhost:8000/api/v1/predict"
MONITORING_URL = "http://localhost:8000/api/v1/flood/monitoring"
DB_NAME = "iot_sensor_data.db"

# Indian Cities with realistic flood risk factors
INDIAN_CITIES = {
    "Mumbai": {"state": "Maharashtra", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Chennai": {"state": "Tamil Nadu", "flood_risk_factor": 0.9, "monsoon_intensity": 0.8},
    "Kolkata": {"state": "West Bengal", "flood_risk_factor": 0.85, "monsoon_intensity": 0.9},
    "Kochi": {"state": "Kerala", "flood_risk_factor": 0.9, "monsoon_intensity": 0.95},
    "Thiruvananthapuram": {"state": "Kerala", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Alappuzha": {"state": "Kerala", "flood_risk_factor": 0.95, "monsoon_intensity": 0.9},
    "Thane": {"state": "Maharashtra", "flood_risk_factor": 0.8, "monsoon_intensity": 0.85},
    "Surat": {"state": "Gujarat", "flood_risk_factor": 0.7, "monsoon_intensity": 0.6},
    "Pune": {"state": "Maharashtra", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Hyderabad": {"state": "Telangana", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Bangalore": {"state": "Karnataka", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Delhi": {"state": "Delhi", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Ahmedabad": {"state": "Gujarat", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Jaipur": {"state": "Rajasthan", "flood_risk_factor": 0.2, "monsoon_intensity": 0.3},
    "Lucknow": {"state": "Uttar Pradesh", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Kanpur": {"state": "Uttar Pradesh", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Nagpur": {"state": "Maharashtra", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Indore": {"state": "Madhya Pradesh", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Bhopal": {"state": "Madhya Pradesh", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Visakhapatnam": {"state": "Andhra Pradesh", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8},
    "Pimpri-Chinchwad": {"state": "Maharashtra", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Patna": {"state": "Bihar", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Vadodara": {"state": "Gujarat", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Coimbatore": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Madurai": {"state": "Tamil Nadu", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Tiruchirappalli": {"state": "Tamil Nadu", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Salem": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Tirunelveli": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Erode": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Vellore": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Thanjavur": {"state": "Tamil Nadu", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Tiruppur": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Dindigul": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Thoothukudi": {"state": "Tamil Nadu", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Hosur": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Nagercoil": {"state": "Tamil Nadu", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Kanchipuram": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Cuddalore": {"state": "Tamil Nadu", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Kumbakonam": {"state": "Tamil Nadu", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Tiruvannamalai": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Pollachi": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Rajapalayam": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Gudiyatham": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Pudukkottai": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Vaniyambadi": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Ambur": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Nagapattinam": {"state": "Tamil Nadu", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Tirupathur": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Karaikudi": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Tiruvallur": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Ranipet": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Arcot": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Arakkonam": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Virudhunagar": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Sivakasi": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Tenkasi": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Palani": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Paramakudi": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Tiruchengode": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Karur": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Valparai": {"state": "Tamil Nadu", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Sankarankovil": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Cumbum": {"state": "Tamil Nadu", "flood_risk_factor": 0.3, "monsoon_intensity": 0.4},
    "Sivaganga": {"state": "Tamil Nadu", "flood_risk_factor": 0.4, "monsoon_intensity": 0.5},
    "Kollam": {"state": "Kerala", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8},
    "Thrissur": {"state": "Kerala", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Palakkad": {"state": "Kerala", "flood_risk_factor": 0.5, "monsoon_intensity": 0.6},
    "Malappuram": {"state": "Kerala", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Kozhikode": {"state": "Kerala", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8},
    "Kannur": {"state": "Kerala", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Kasaragod": {"state": "Kerala", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8},
    "Pathanamthitta": {"state": "Kerala", "flood_risk_factor": 0.6, "monsoon_intensity": 0.7},
    "Kottayam": {"state": "Kerala", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8},
    "Idukki": {"state": "Kerala", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Ernakulam": {"state": "Kerala", "flood_risk_factor": 0.8, "monsoon_intensity": 0.9},
    "Wayanad": {"state": "Kerala", "flood_risk_factor": 0.7, "monsoon_intensity": 0.8}
}

# ---------------------------
# Helper Functions
# ---------------------------
def get_current_time():
    """Get current IST time."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def init_database():
    """Initialize IoT sensor database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            state TEXT,
            water_level INTEGER,
            rainfall INTEGER,
            river_flow INTEGER,
            risk_level TEXT,
            confidence REAL,
            timestamp TEXT,
            sent_to_api BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()

def save_sensor_data(city: str, sensor_data: Dict, prediction: Dict = None):
    """Save sensor data to database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (city, state, water_level, rainfall, river_flow, 
                               risk_level, confidence, timestamp, sent_to_api)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        city,
        INDIAN_CITIES[city]["state"],
        sensor_data["water_level"],
        sensor_data["rainfall"],
        sensor_data["river_flow"],
        prediction["risk_level"] if prediction else "UNKNOWN",
        prediction["confidence"] if prediction else 0.0,
        sensor_data["timestamp"],
        prediction is not None
    ))
    conn.commit()
    conn.close()

def generate_realistic_sensor_data(city: str) -> Dict:
    """Generate realistic sensor data for a city."""
    city_info = INDIAN_CITIES[city]
    flood_risk_factor = city_info["flood_risk_factor"]
    monsoon_intensity = city_info["monsoon_intensity"]
    
    # Base values
    base_water_level = random.randint(0, 30)
    base_rainfall = random.randint(0, 50)
    base_river_flow = random.randint(0, 100)
    
    # Adjust based on flood risk factor and monsoon intensity
    water_level = min(150, int(base_water_level + (flood_risk_factor * 80) + (monsoon_intensity * 40)))
    rainfall = min(400, int(base_rainfall + (flood_risk_factor * 200) + (monsoon_intensity * 150)))
    river_flow = min(800, int(base_river_flow + (flood_risk_factor * 400) + (monsoon_intensity * 300)))
    
    # Add some randomness for realistic variation
    water_level += random.randint(-10, 10)
    rainfall += random.randint(-20, 20)
    river_flow += random.randint(-50, 50)
    
    # Ensure non-negative values
    water_level = max(0, water_level)
    rainfall = max(0, rainfall)
    river_flow = max(0, river_flow)
    
    return {
        "city": city,
        "water_level": water_level,
        "rainfall": rainfall,
        "river_flow": river_flow,
        "timestamp": get_current_time()
    }

def send_to_fastapi(sensor_data: Dict) -> Dict:
    """Send sensor data to FastAPI backend."""
    try:
        response = requests.post(
            FASTAPI_URL,
            json=sensor_data,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Connection error: {e}")
        return None

def get_monitoring_status() -> Dict:
    """Get current monitoring status from FastAPI."""
    try:
        response = requests.get(MONITORING_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def simulate_city_monitoring(city: str, interval: int = 30):
    """Simulate monitoring for a specific city."""
    print(f"🌊 Starting IoT simulation for {city}...")
    
    while True:
        try:
            # Generate sensor data
            sensor_data = generate_realistic_sensor_data(city)
            
            print(f"\n📡 {city} Sensor Data:")
            print(f"   💧 Water Level: {sensor_data['water_level']} cm")
            print(f"   🌧️ Rainfall: {sensor_data['rainfall']} mm")
            print(f"   🌊 River Flow: {sensor_data['river_flow']} m³/s")
            print(f"   ⏰ Time: {sensor_data['timestamp']}")
            
            # Send to FastAPI
            prediction = send_to_fastapi(sensor_data)
            
            if prediction:
                print(f"   🔎 Risk Assessment: {prediction['risk_level']}")
                print(f"   📊 Confidence: {prediction['confidence']}%")
                print(f"   📌 Reason: {prediction['reason']}")
                print(f"   📝 Recommendation: {prediction['recommendation']}")
                
                if prediction['risk_level'] == 'HIGH':
                    print("🚨 HIGH FLOOD RISK DETECTED - IMMEDIATE ACTION REQUIRED 🚨")
                    print(f"   ☎️ Emergency Helplines:\n{prediction['helpline']}")
                
                # Save to database
                save_sensor_data(city, sensor_data, prediction)
                
            else:
                print("   ⚠️ Failed to get prediction from API")
                save_sensor_data(city, sensor_data)
            
            # Wait before next reading
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print(f"\n🛑 Stopping simulation for {city}")
            break
        except Exception as e:
            print(f"❌ Error in {city} simulation: {e}")
            time.sleep(5)

def run_multi_city_simulation():
    """Run simulation for multiple cities simultaneously."""
    print("🌊 JalRakshā AI - Enhanced IoT Flood Monitoring Simulator")
    print("=" * 60)
    print(f"📊 Monitoring {len(INDIAN_CITIES)} Indian cities")
    print(f"🔗 FastAPI Backend: {FASTAPI_URL}")
    print(f"📱 Monitoring API: {MONITORING_URL}")
    print("=" * 60)
    
    # Initialize database
    init_database()
    
    # Start monitoring threads for each city
    threads = []
    
    for city in INDIAN_CITIES.keys():
        # Random interval between 20-60 seconds for each city
        interval = random.randint(20, 60)
        thread = threading.Thread(
            target=simulate_city_monitoring,
            args=(city, interval),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        print(f"🚀 Started monitoring thread for {city} (interval: {interval}s)")
        time.sleep(1)  # Stagger thread starts
    
    print(f"\n✅ All {len(threads)} monitoring threads started successfully!")
    print("🔄 Real-time flood monitoring is now active...")
    print("📱 Check the React frontend at http://localhost:3000")
    print("🔧 API documentation at http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all monitoring...")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(10)
            
            # Show periodic status update
            status = get_monitoring_status()
            if status:
                print(f"\n📊 Status Update:")
                print(f"   🏙️ Cities Monitored: {status['total_cities']}")
                print(f"   🔥 High Risk: {status['high_risk_count']}")
                print(f"   ⚠️ Medium Risk: {status['medium_risk_count']}")
                print(f"   ✅ Low Risk: {status['low_risk_count']}")
                print(f"   ⏰ Last Updated: {status['last_updated']}")
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down IoT simulator...")
        print("👋 All monitoring threads stopped. Goodbye!")

def run_single_city_simulation(city: str = None):
    """Run simulation for a single city."""
    if not city:
        city = random.choice(list(INDIAN_CITIES.keys()))
    
    if city not in INDIAN_CITIES:
        print(f"❌ City '{city}' not found in database")
        return
    
    print(f"🌊 Single City IoT Simulation: {city}")
    print("=" * 40)
    
    init_database()
    simulate_city_monitoring(city, 15)  # 15-second intervals for single city

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--single":
            city = sys.argv[2] if len(sys.argv) > 2 else None
            run_single_city_simulation(city)
        elif sys.argv[1] == "--help":
            print("🌊 JalRakshā AI IoT Simulator")
            print("\nUsage:")
            print("  python enhanced_iot_simulator.py              # Run multi-city simulation")
            print("  python enhanced_iot_simulator.py --single      # Run single city simulation")
            print("  python enhanced_iot_simulator.py --single Mumbai  # Run simulation for Mumbai")
            print("  python enhanced_iot_simulator.py --help       # Show this help")
            print(f"\nAvailable cities: {', '.join(INDIAN_CITIES.keys())}")
        else:
            print("❌ Unknown argument. Use --help for usage information.")
    else:
        run_multi_city_simulation()
