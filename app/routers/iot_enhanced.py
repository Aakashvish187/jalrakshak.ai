"""
🌊 JalRakshā AI - Enhanced IoT Router
Advanced IoT sensor management with LoRaWAN/MQTT support and health monitoring
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sqlite3
import json
import logging
import asyncio
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/iot", tags=["iot"])

@dataclass
class SensorNode:
    """IoT Sensor Node"""
    node_id: str
    name: str
    lat: float
    lng: float
    sensor_type: str
    protocol: str
    status: str
    health_score: int
    last_seen: Optional[datetime]
    data: Dict[str, Any]

class SensorDataRequest(BaseModel):
    """Sensor data request model"""
    node_id: str
    protocol: str
    timestamp: str
    data: Dict[str, Any]

class SensorHealthRequest(BaseModel):
    """Sensor health request model"""
    node_id: str
    status: str
    health_score: int
    battery_level: Optional[float] = None
    signal_strength: Optional[float] = None
    error_count: Optional[int] = None

class IoTProtocolManager:
    """IoT Protocol Manager for handling different protocols"""
    
    def __init__(self):
        self.database_path = "iot_sensors.db"
        self.init_database()
        self.active_sensors: Dict[str, SensorNode] = {}
    
    def init_database(self):
        """Initialize IoT sensors database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Sensors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensors (
                    node_id TEXT PRIMARY KEY,
                    name TEXT,
                    lat REAL,
                    lng REAL,
                    sensor_type TEXT,
                    protocol TEXT,
                    status TEXT,
                    health_score INTEGER,
                    last_seen TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sensor data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    sensor_type TEXT,
                    data_value REAL,
                    unit TEXT,
                    quality TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (node_id) REFERENCES sensors (node_id)
                )
            ''')
            
            # Sensor health table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    status TEXT,
                    health_score INTEGER,
                    battery_level REAL,
                    signal_strength REAL,
                    error_count INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (node_id) REFERENCES sensors (node_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ IoT sensors database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
    
    async def register_sensor(self, sensor: SensorNode) -> bool:
        """Register a new sensor"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sensors 
                (node_id, name, lat, lng, sensor_type, protocol, status, health_score, last_seen, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sensor.node_id, sensor.name, sensor.lat, sensor.lng,
                sensor.sensor_type, sensor.protocol, sensor.status,
                sensor.health_score, sensor.last_seen.isoformat() if sensor.last_seen else None,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            self.active_sensors[sensor.node_id] = sensor
            logger.info(f"✅ Sensor {sensor.node_id} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Register sensor error: {str(e)}")
            return False
    
    async def store_sensor_data(self, node_id: str, data: Dict[str, Any]) -> bool:
        """Store sensor data"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get sensor info
            cursor.execute("SELECT sensor_type FROM sensors WHERE node_id = ?", (node_id,))
            result = cursor.fetchone()
            
            if result:
                sensor_type = result[0]
                
                cursor.execute('''
                    INSERT INTO sensor_data (node_id, sensor_type, data_value, unit, quality)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    node_id, sensor_type,
                    data.get("value", 0),
                    data.get("unit", "unknown"),
                    data.get("quality", "unknown")
                ))
                
                # Update sensor last_seen
                cursor.execute('''
                    UPDATE sensors SET last_seen = ?, updated_at = ?
                    WHERE node_id = ?
                ''', (datetime.now().isoformat(), datetime.now().isoformat(), node_id))
                
                conn.commit()
                conn.close()
                
                logger.info(f"✅ Sensor data stored for {node_id}")
                return True
            else:
                logger.error(f"❌ Sensor {node_id} not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Store sensor data error: {str(e)}")
            return False
    
    async def update_sensor_health(self, node_id: str, health_data: Dict[str, Any]) -> bool:
        """Update sensor health status"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sensor_health 
                (node_id, status, health_score, battery_level, signal_strength, error_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                node_id,
                health_data.get("status", "unknown"),
                health_data.get("health_score", 0),
                health_data.get("battery_level"),
                health_data.get("signal_strength"),
                health_data.get("error_count")
            ))
            
            # Update sensor status
            cursor.execute('''
                UPDATE sensors SET status = ?, health_score = ?, updated_at = ?
                WHERE node_id = ?
            ''', (
                health_data.get("status", "unknown"),
                health_data.get("health_score", 0),
                datetime.now().isoformat(),
                node_id
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Sensor health updated for {node_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Update sensor health error: {str(e)}")
            return False
    
    async def get_all_sensors(self) -> List[Dict[str, Any]]:
        """Get all registered sensors"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT node_id, name, lat, lng, sensor_type, protocol, 
                       status, health_score, last_seen
                FROM sensors
                ORDER BY updated_at DESC
            ''')
            
            sensors = []
            for row in cursor.fetchall():
                sensors.append({
                    "node_id": row[0],
                    "name": row[1],
                    "lat": row[2],
                    "lng": row[3],
                    "sensor_type": row[4],
                    "protocol": row[5],
                    "status": row[6],
                    "health_score": row[7],
                    "last_seen": row[8],
                    "data": {}  # Will be populated with latest data
                })
            
            conn.close()
            return sensors
            
        except Exception as e:
            logger.error(f"❌ Get all sensors error: {str(e)}")
            return []
    
    async def get_sensor_health_summary(self) -> Dict[str, Any]:
        """Get sensor network health summary"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get status counts
            cursor.execute('''
                SELECT status, COUNT(*) FROM sensors GROUP BY status
            ''')
            status_counts = dict(cursor.fetchall())
            
            # Get average health score
            cursor.execute('''
                SELECT AVG(health_score) FROM sensors WHERE health_score > 0
            ''')
            avg_health_score = cursor.fetchone()[0] or 0
            
            # Get protocol distribution
            cursor.execute('''
                SELECT protocol, COUNT(*) FROM sensors GROUP BY protocol
            ''')
            protocol_distribution = dict(cursor.fetchall())
            
            # Get sensor type distribution
            cursor.execute('''
                SELECT sensor_type, COUNT(*) FROM sensors GROUP BY sensor_type
            ''')
            sensor_type_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "total_sensors": sum(status_counts.values()),
                "online_count": status_counts.get("online", 0),
                "offline_count": status_counts.get("offline", 0),
                "error_count": status_counts.get("error", 0),
                "avg_health_score": round(avg_health_score, 2),
                "protocol_distribution": protocol_distribution,
                "sensor_type_distribution": sensor_type_distribution,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Get sensor health summary error: {str(e)}")
            return {}

# Global IoT Protocol Manager
iot_manager = IoTProtocolManager()

@router.post("/sensor-data")
async def receive_sensor_data(request: SensorDataRequest, background_tasks: BackgroundTasks):
    """Receive sensor data from IoT devices"""
    try:
        # Store sensor data in background
        background_tasks.add_task(
            iot_manager.store_sensor_data,
            request.node_id,
            request.data
        )
        
        logger.info(f"📡 Received sensor data from {request.node_id} via {request.protocol}")
        
        return {
            "status": "success",
            "message": f"Sensor data received from {request.node_id}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Receive sensor data error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sensor-health")
async def update_sensor_health(request: SensorHealthRequest, background_tasks: BackgroundTasks):
    """Update sensor health status"""
    try:
        health_data = {
            "status": request.status,
            "health_score": request.health_score,
            "battery_level": request.battery_level,
            "signal_strength": request.signal_strength,
            "error_count": request.error_count
        }
        
        # Update sensor health in background
        background_tasks.add_task(
            iot_manager.update_sensor_health,
            request.node_id,
            health_data
        )
        
        logger.info(f"🏥 Updated health status for {request.node_id}: {request.status}")
        
        return {
            "status": "success",
            "message": f"Health status updated for {request.node_id}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Update sensor health error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensors")
async def get_all_sensors():
    """Get all registered IoT sensors"""
    try:
        sensors = await iot_manager.get_all_sensors()
        
        return {
            "status": "success",
            "sensors": sensors,
            "count": len(sensors),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Get all sensors error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensor-health")
async def get_sensor_health():
    """Get sensor network health summary"""
    try:
        health_summary = await iot_manager.get_sensor_health_summary()
        
        return {
            "status": "success",
            "health_summary": health_summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Get sensor health error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensors/{node_id}")
async def get_sensor_details(node_id: str):
    """Get detailed information about a specific sensor"""
    try:
        conn = sqlite3.connect(iot_manager.database_path)
        cursor = conn.cursor()
        
        # Get sensor info
        cursor.execute('''
            SELECT node_id, name, lat, lng, sensor_type, protocol, 
                   status, health_score, last_seen, created_at
            FROM sensors WHERE node_id = ?
        ''', (node_id,))
        
        sensor_info = cursor.fetchone()
        
        if not sensor_info:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get recent data
        cursor.execute('''
            SELECT data_value, unit, quality, timestamp
            FROM sensor_data 
            WHERE node_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (node_id,))
        
        recent_data = cursor.fetchall()
        
        # Get health history
        cursor.execute('''
            SELECT status, health_score, battery_level, signal_strength, timestamp
            FROM sensor_health 
            WHERE node_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (node_id,))
        
        health_history = cursor.fetchall()
        
        conn.close()
        
        return {
            "status": "success",
            "sensor": {
                "node_id": sensor_info[0],
                "name": sensor_info[1],
                "lat": sensor_info[2],
                "lng": sensor_info[3],
                "sensor_type": sensor_info[4],
                "protocol": sensor_info[5],
                "status": sensor_info[6],
                "health_score": sensor_info[7],
                "last_seen": sensor_info[8],
                "created_at": sensor_info[9]
            },
            "recent_data": [
                {
                    "value": row[0],
                    "unit": row[1],
                    "quality": row[2],
                    "timestamp": row[3]
                } for row in recent_data
            ],
            "health_history": [
                {
                    "status": row[0],
                    "health_score": row[1],
                    "battery_level": row[2],
                    "signal_strength": row[3],
                    "timestamp": row[4]
                } for row in health_history
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Get sensor details error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register-sensor")
async def register_sensor(
    node_id: str,
    name: str,
    lat: float,
    lng: float,
    sensor_type: str,
    protocol: str
):
    """Register a new IoT sensor"""
    try:
        sensor = SensorNode(
            node_id=node_id,
            name=name,
            lat=lat,
            lng=lng,
            sensor_type=sensor_type,
            protocol=protocol,
            status="offline",
            health_score=0,
            last_seen=None,
            data={}
        )
        
        success = await iot_manager.register_sensor(sensor)
        
        if success:
            return {
                "status": "success",
                "message": f"Sensor {node_id} registered successfully",
                "sensor": {
                    "node_id": node_id,
                    "name": name,
                    "lat": lat,
                    "lng": lng,
                    "sensor_type": sensor_type,
                    "protocol": protocol,
                    "status": "offline"
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to register sensor")
            
    except Exception as e:
        logger.error(f"❌ Register sensor error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/protocols")
async def get_supported_protocols():
    """Get list of supported IoT protocols"""
    return {
        "status": "success",
        "protocols": [
            {
                "name": "MQTT",
                "description": "Message Queuing Telemetry Transport",
                "features": ["Lightweight", "Publish/Subscribe", "QoS Support"],
                "port": 1883,
                "secure_port": 8883
            },
            {
                "name": "LoRaWAN",
                "description": "Long Range Wide Area Network",
                "features": ["Low Power", "Long Range", "Secure"],
                "frequency": "868 MHz (India)",
                "spreading_factors": [7, 8, 9, 10, 11, 12]
            },
            {
                "name": "HTTP",
                "description": "Hypertext Transfer Protocol",
                "features": ["RESTful", "Simple", "Widely Supported"],
                "port": 80,
                "secure_port": 443
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/sensor-types")
async def get_sensor_types():
    """Get list of supported sensor types"""
    return {
        "status": "success",
        "sensor_types": [
            {
                "type": "water_level",
                "name": "Water Level Sensor",
                "unit": "meters",
                "range": "0-15m",
                "description": "Measures water level in rivers, lakes, and reservoirs"
            },
            {
                "type": "rainfall",
                "name": "Rainfall Sensor",
                "unit": "mm/hour",
                "range": "0-200mm/hr",
                "description": "Measures rainfall intensity and accumulation"
            },
            {
                "type": "river_flow",
                "name": "River Flow Sensor",
                "unit": "ratio",
                "range": "0-1",
                "description": "Measures river flow rate and velocity"
            },
            {
                "type": "drainage",
                "name": "Drainage Capacity Sensor",
                "unit": "ratio",
                "range": "0-1",
                "description": "Monitors drainage system capacity and efficiency"
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

