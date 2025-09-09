"""
🌊 JalRakshā AI - Advanced IoT Protocol Handler
Supports LoRaWAN, MQTT, and HTTP protocols for real IoT sensor integration
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import paho.mqtt.client as mqtt
import requests
from dataclasses import dataclass
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SensorNode:
    """IoT Sensor Node Configuration"""
    node_id: str
    name: str
    lat: float
    lng: float
    sensor_type: str  # 'water_level', 'rainfall', 'river_flow', 'drainage'
    protocol: str  # 'lorawan', 'mqtt', 'http'
    connection_params: Dict[str, Any]
    last_seen: Optional[datetime] = None
    status: str = 'offline'  # 'online', 'offline', 'error'
    data: Dict[str, Any] = None

class LoRaWANHandler:
    """LoRaWAN Protocol Handler for IoT Sensors"""
    
    def __init__(self):
        self.gateway_url = "http://localhost:8080/api/lorawan"  # LoRaWAN Gateway
        self.active_nodes: Dict[str, SensorNode] = {}
    
    async def register_node(self, node: SensorNode) -> bool:
        """Register a LoRaWAN sensor node"""
        try:
            payload = {
                "node_id": node.node_id,
                "name": node.name,
                "location": {"lat": node.lat, "lng": node.lng},
                "sensor_type": node.sensor_type,
                "frequency": node.connection_params.get("frequency", "868.1"),
                "spreading_factor": node.connection_params.get("spreading_factor", 7)
            }
            
            response = requests.post(f"{self.gateway_url}/register", json=payload, timeout=5)
            if response.status_code == 200:
                self.active_nodes[node.node_id] = node
                logger.info(f"✅ LoRaWAN node {node.node_id} registered successfully")
                return True
            else:
                logger.error(f"❌ Failed to register LoRaWAN node {node.node_id}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ LoRaWAN registration error for {node.node_id}: {str(e)}")
            return False
    
    async def receive_data(self, node_id: str, data: Dict[str, Any]) -> bool:
        """Receive data from LoRaWAN sensor"""
        try:
            if node_id in self.active_nodes:
                node = self.active_nodes[node_id]
                node.last_seen = datetime.now()
                node.status = 'online'
                node.data = data
                
                # Forward to main system
                await self.forward_to_system(node_id, data)
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ LoRaWAN data receive error for {node_id}: {str(e)}")
            return False
    
    async def forward_to_system(self, node_id: str, data: Dict[str, Any]):
        """Forward LoRaWAN data to main JalRakshā system"""
        try:
            payload = {
                "node_id": node_id,
                "protocol": "lorawan",
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            response = requests.post("http://localhost:8000/api/v1/iot/sensor-data", 
                                  json=payload, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ LoRaWAN data forwarded for {node_id}")
            else:
                logger.error(f"❌ Failed to forward LoRaWAN data for {node_id}")
                
        except Exception as e:
            logger.error(f"❌ LoRaWAN forward error for {node_id}: {str(e)}")

class MQTTHandler:
    """MQTT Protocol Handler for IoT Sensors"""
    
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.active_nodes: Dict[str, SensorNode] = {}
        self.setup_mqtt_client()
    
    def setup_mqtt_client(self):
        """Setup MQTT client with callbacks"""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("✅ MQTT broker connected successfully")
            # Subscribe to all JalRakshā sensor topics
            client.subscribe("jalraksha/sensors/+/data")
            client.subscribe("jalraksha/sensors/+/status")
        else:
            logger.error(f"❌ MQTT connection failed with code {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT message callback"""
        try:
            topic_parts = msg.topic.split('/')
            if len(topic_parts) >= 4:
                node_id = topic_parts[2]
                message_type = topic_parts[3]
                
                data = json.loads(msg.payload.decode())
                
                if message_type == "data":
                    asyncio.create_task(self.handle_sensor_data(node_id, data))
                elif message_type == "status":
                    asyncio.create_task(self.handle_status_update(node_id, data))
                    
        except Exception as e:
            logger.error(f"❌ MQTT message processing error: {str(e)}")
    
    def on_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        logger.warning("⚠️ MQTT broker disconnected")
    
    async def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            logger.info(f"✅ MQTT client connected to {self.broker_host}:{self.broker_port}")
        except Exception as e:
            logger.error(f"❌ MQTT connection error: {str(e)}")
    
    async def register_node(self, node: SensorNode) -> bool:
        """Register an MQTT sensor node"""
        try:
            self.active_nodes[node.node_id] = node
            
            # Subscribe to node-specific topics
            self.client.subscribe(f"jalraksha/sensors/{node.node_id}/data")
            self.client.subscribe(f"jalraksha/sensors/{node.node_id}/status")
            
            logger.info(f"✅ MQTT node {node.node_id} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ MQTT registration error for {node.node_id}: {str(e)}")
            return False
    
    async def handle_sensor_data(self, node_id: str, data: Dict[str, Any]):
        """Handle incoming sensor data from MQTT"""
        try:
            if node_id in self.active_nodes:
                node = self.active_nodes[node_id]
                node.last_seen = datetime.now()
                node.status = 'online'
                node.data = data
                
                # Forward to main system
                await self.forward_to_system(node_id, data)
                
        except Exception as e:
            logger.error(f"❌ MQTT sensor data error for {node_id}: {str(e)}")
    
    async def handle_status_update(self, node_id: str, data: Dict[str, Any]):
        """Handle sensor status updates from MQTT"""
        try:
            if node_id in self.active_nodes:
                node = self.active_nodes[node_id]
                node.status = data.get('status', 'unknown')
                node.last_seen = datetime.now()
                
        except Exception as e:
            logger.error(f"❌ MQTT status update error for {node_id}: {str(e)}")
    
    async def forward_to_system(self, node_id: str, data: Dict[str, Any]):
        """Forward MQTT data to main JalRakshā system"""
        try:
            payload = {
                "node_id": node_id,
                "protocol": "mqtt",
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            response = requests.post("http://localhost:8000/api/v1/iot/sensor-data", 
                                  json=payload, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ MQTT data forwarded for {node_id}")
            else:
                logger.error(f"❌ Failed to forward MQTT data for {node_id}")
                
        except Exception as e:
            logger.error(f"❌ MQTT forward error for {node_id}: {str(e)}")

class SensorHealthMonitor:
    """Monitor sensor health and connectivity status"""
    
    def __init__(self):
        self.health_check_interval = 30  # seconds
        self.timeout_threshold = 300  # 5 minutes
        self.sensor_database = "sensor_health.db"
        self.init_database()
    
    def init_database(self):
        """Initialize sensor health database"""
        try:
            conn = sqlite3.connect(self.sensor_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_health (
                    node_id TEXT PRIMARY KEY,
                    name TEXT,
                    sensor_type TEXT,
                    protocol TEXT,
                    status TEXT,
                    last_seen TIMESTAMP,
                    health_score INTEGER,
                    error_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Sensor health database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
    
    async def check_sensor_health(self, node: SensorNode) -> Dict[str, Any]:
        """Check individual sensor health"""
        try:
            current_time = datetime.now()
            health_score = 100
            
            # Check if sensor is responsive
            if node.last_seen:
                time_diff = (current_time - node.last_seen).total_seconds()
                
                if time_diff > self.timeout_threshold:
                    node.status = 'offline'
                    health_score = 0
                elif time_diff > 60:  # 1 minute
                    health_score = 50
                elif time_diff > 30:  # 30 seconds
                    health_score = 75
            else:
                node.status = 'offline'
                health_score = 0
            
            # Update database
            await self.update_health_database(node, health_score)
            
            return {
                "node_id": node.node_id,
                "status": node.status,
                "health_score": health_score,
                "last_seen": node.last_seen.isoformat() if node.last_seen else None,
                "response_time": time_diff if node.last_seen else None
            }
            
        except Exception as e:
            logger.error(f"❌ Health check error for {node.node_id}: {str(e)}")
            return {"node_id": node.node_id, "status": "error", "health_score": 0}
    
    async def update_health_database(self, node: SensorNode, health_score: int):
        """Update sensor health in database"""
        try:
            conn = sqlite3.connect(self.sensor_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sensor_health 
                (node_id, name, sensor_type, protocol, status, last_seen, health_score, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                node.node_id,
                node.name,
                node.sensor_type,
                node.protocol,
                node.status,
                node.last_seen.isoformat() if node.last_seen else None,
                health_score,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Database update error: {str(e)}")
    
    async def get_all_sensor_health(self) -> List[Dict[str, Any]]:
        """Get health status of all sensors"""
        try:
            conn = sqlite3.connect(self.sensor_database)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT node_id, name, sensor_type, protocol, status, 
                       last_seen, health_score, error_count
                FROM sensor_health
                ORDER BY health_score DESC, updated_at DESC
            ''')
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "node_id": row[0],
                    "name": row[1],
                    "sensor_type": row[2],
                    "protocol": row[3],
                    "status": row[4],
                    "last_seen": row[5],
                    "health_score": row[6],
                    "error_count": row[7]
                })
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"❌ Get health status error: {str(e)}")
            return []

class IoTProtocolManager:
    """Main IoT Protocol Manager - Coordinates all protocols"""
    
    def __init__(self):
        self.lorawan_handler = LoRaWANHandler()
        self.mqtt_handler = MQTTHandler()
        self.health_monitor = SensorHealthMonitor()
        self.all_nodes: Dict[str, SensorNode] = {}
        
    async def initialize(self):
        """Initialize all IoT protocol handlers"""
        try:
            # Connect MQTT
            await self.mqtt_handler.connect()
            
            # Register sample sensors
            await self.register_sample_sensors()
            
            logger.info("✅ IoT Protocol Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ IoT Protocol Manager initialization error: {str(e)}")
    
    async def register_sample_sensors(self):
        """Register sample IoT sensors across India"""
        sample_sensors = [
            # Water Level Sensors
            SensorNode("WL001", "Ganga River Gauge - Patna", 25.5941, 85.1376, 
                      "water_level", "mqtt", {"topic": "jalraksha/sensors/WL001/data"}),
            SensorNode("WL002", "Yamuna River Gauge - Delhi", 28.7041, 77.1025, 
                      "water_level", "lorawan", {"frequency": "868.1", "spreading_factor": 7}),
            SensorNode("WL003", "Krishna River Gauge - Vijayawada", 16.5062, 80.6480, 
                      "water_level", "mqtt", {"topic": "jalraksha/sensors/WL003/data"}),
            
            # Rainfall Sensors
            SensorNode("RF001", "Mumbai Rainfall Station", 19.0760, 72.8777, 
                      "rainfall", "mqtt", {"topic": "jalraksha/sensors/RF001/data"}),
            SensorNode("RF002", "Chennai Rainfall Station", 13.0827, 80.2707, 
                      "rainfall", "lorawan", {"frequency": "868.3", "spreading_factor": 8}),
            SensorNode("RF003", "Kolkata Rainfall Station", 22.5726, 88.3639, 
                      "rainfall", "mqtt", {"topic": "jalraksha/sensors/RF003/data"}),
            
            # River Flow Sensors
            SensorNode("RF004", "Brahmaputra Flow - Guwahati", 26.1445, 91.7362, 
                      "river_flow", "lorawan", {"frequency": "868.5", "spreading_factor": 7}),
            SensorNode("RF005", "Godavari Flow - Rajahmundry", 17.0005, 81.8040, 
                      "river_flow", "mqtt", {"topic": "jalraksha/sensors/RF005/data"}),
            
            # Drainage Capacity Sensors
            SensorNode("DC001", "Delhi Drainage Monitor", 28.6139, 77.2090, 
                      "drainage", "mqtt", {"topic": "jalraksha/sensors/DC001/data"}),
            SensorNode("DC002", "Bangalore Drainage Monitor", 12.9716, 77.5946, 
                      "drainage", "lorawan", {"frequency": "868.7", "spreading_factor": 8}),
        ]
        
        for sensor in sample_sensors:
            self.all_nodes[sensor.node_id] = sensor
            
            if sensor.protocol == "mqtt":
                await self.mqtt_handler.register_node(sensor)
            elif sensor.protocol == "lorawan":
                await self.lorawan_handler.register_node(sensor)
    
    async def get_sensor_map_data(self) -> List[Dict[str, Any]]:
        """Get sensor data for map visualization"""
        try:
            sensor_data = []
            
            for node_id, node in self.all_nodes.items():
                health_info = await self.health_monitor.check_sensor_health(node)
                
                sensor_data.append({
                    "node_id": node.node_id,
                    "name": node.name,
                    "lat": node.lat,
                    "lng": node.lng,
                    "sensor_type": node.sensor_type,
                    "protocol": node.protocol,
                    "status": node.status,
                    "health_score": health_info.get("health_score", 0),
                    "last_seen": node.last_seen.isoformat() if node.last_seen else None,
                    "data": node.data or {}
                })
            
            return sensor_data
            
        except Exception as e:
            logger.error(f"❌ Get sensor map data error: {str(e)}")
            return []
    
    async def start_health_monitoring(self):
        """Start continuous health monitoring"""
        while True:
            try:
                logger.info("🔍 Running sensor health check...")
                
                for node_id, node in self.all_nodes.items():
                    await self.health_monitor.check_sensor_health(node)
                
                await asyncio.sleep(self.health_monitor.health_check_interval)
                
            except Exception as e:
                logger.error(f"❌ Health monitoring error: {str(e)}")
                await asyncio.sleep(10)

# Main execution
async def main():
    """Main IoT Protocol Manager execution"""
    logger.info("🌊 Starting JalRakshā AI IoT Protocol Manager...")
    
    manager = IoTProtocolManager()
    await manager.initialize()
    
    # Start health monitoring in background
    asyncio.create_task(manager.start_health_monitoring())
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 IoT Protocol Manager stopped")

if __name__ == "__main__":
    asyncio.run(main())

