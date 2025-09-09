"""
🌊 JalRakshā AI - Enhanced IoT Simulator V2
Advanced simulation with LoRaWAN/MQTT protocols and real-time sensor health monitoring
"""

import asyncio
import json
import random
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import sqlite3
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SensorSimulation:
    """Sensor simulation configuration"""
    node_id: str
    name: str
    city: str
    lat: float
    lng: float
    sensor_type: str
    protocol: str
    base_value: float
    variation_range: float
    trend_factor: float
    last_value: float = 0.0
    last_update: Optional[datetime] = None

class IoTProtocolSimulator:
    """Simulate different IoT protocols (LoRaWAN, MQTT, HTTP)"""
    
    def __init__(self):
        self.mqtt_broker = "localhost"
        self.mqtt_port = 1883
        self.lorawan_gateway = "http://localhost:8080/api/lorawan"
        self.http_endpoint = "http://localhost:8000/api/v1/iot/sensor-data"
        
    async def simulate_mqtt_sensor(self, sensor: SensorSimulation) -> Dict[str, Any]:
        """Simulate MQTT sensor data transmission"""
        try:
            # Generate realistic sensor data
            sensor_data = await self.generate_sensor_data(sensor)
            
            # Simulate MQTT message format
            mqtt_message = {
                "topic": f"jalraksha/sensors/{sensor.node_id}/data",
                "payload": {
                    "node_id": sensor.node_id,
                    "timestamp": datetime.now().isoformat(),
                    "sensor_type": sensor.sensor_type,
                    "data": sensor_data,
                    "battery_level": random.uniform(20, 100),
                    "signal_strength": random.uniform(-80, -30),
                    "packet_loss": random.uniform(0, 5)
                },
                "qos": 1,
                "retain": False
            }
            
            # Simulate network delay
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Forward to main system
            await self.forward_to_system(sensor.node_id, sensor_data, "mqtt")
            
            logger.info(f"📡 MQTT sensor {sensor.node_id} transmitted data")
            return mqtt_message
            
        except Exception as e:
            logger.error(f"❌ MQTT simulation error for {sensor.node_id}: {str(e)}")
            return {}
    
    async def simulate_lorawan_sensor(self, sensor: SensorSimulation) -> Dict[str, Any]:
        """Simulate LoRaWAN sensor data transmission"""
        try:
            # Generate realistic sensor data
            sensor_data = await self.generate_sensor_data(sensor)
            
            # Simulate LoRaWAN packet format
            lorawan_packet = {
                "gateway_id": f"GW_{random.randint(1000, 9999)}",
                "node_id": sensor.node_id,
                "timestamp": datetime.now().isoformat(),
                "frequency": random.choice(["868.1", "868.3", "868.5"]),
                "spreading_factor": random.choice([7, 8, 9]),
                "coding_rate": "4/5",
                "rssi": random.uniform(-120, -60),
                "snr": random.uniform(-20, 20),
                "data": {
                    "sensor_type": sensor.sensor_type,
                    "value": sensor_data,
                    "battery_level": random.uniform(15, 95),
                    "temperature": random.uniform(-10, 50)
                }
            }
            
            # Simulate LoRaWAN transmission delay
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Forward to main system
            await self.forward_to_system(sensor.node_id, sensor_data, "lorawan")
            
            logger.info(f"📡 LoRaWAN sensor {sensor.node_id} transmitted data")
            return lorawan_packet
            
        except Exception as e:
            logger.error(f"❌ LoRaWAN simulation error for {sensor.node_id}: {str(e)}")
            return {}
    
    async def simulate_http_sensor(self, sensor: SensorSimulation) -> Dict[str, Any]:
        """Simulate HTTP sensor data transmission"""
        try:
            # Generate realistic sensor data
            sensor_data = await self.generate_sensor_data(sensor)
            
            # Simulate HTTP request
            http_request = {
                "method": "POST",
                "url": self.http_endpoint,
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer sensor_{sensor.node_id}",
                    "User-Agent": f"IoT-Sensor/{sensor.node_id}"
                },
                "payload": {
                    "node_id": sensor.node_id,
                    "protocol": "http",
                    "timestamp": datetime.now().isoformat(),
                    "data": sensor_data,
                    "location": {
                        "lat": sensor.lat,
                        "lng": sensor.lng
                    },
                    "metadata": {
                        "firmware_version": "1.2.3",
                        "uptime": random.randint(1000, 86400),
                        "error_count": random.randint(0, 5)
                    }
                }
            }
            
            # Simulate HTTP transmission
            await asyncio.sleep(random.uniform(0.2, 1.0))
            
            # Forward to main system
            await self.forward_to_system(sensor.node_id, sensor_data, "http")
            
            logger.info(f"📡 HTTP sensor {sensor.node_id} transmitted data")
            return http_request
            
        except Exception as e:
            logger.error(f"❌ HTTP simulation error for {sensor.node_id}: {str(e)}")
            return {}
    
    async def generate_sensor_data(self, sensor: SensorSimulation) -> Dict[str, Any]:
        """Generate realistic sensor data based on type"""
        try:
            current_time = datetime.now()
            
            # Apply trend and variation
            trend = sensor.trend_factor * (current_time.hour / 24.0)  # Daily trend
            variation = random.uniform(-sensor.variation_range, sensor.variation_range)
            new_value = sensor.base_value + trend + variation
            
            # Ensure realistic bounds
            if sensor.sensor_type == "water_level":
                new_value = max(0, min(15, new_value))  # 0-15 meters
                unit = "m"
            elif sensor.sensor_type == "rainfall":
                new_value = max(0, min(200, new_value))  # 0-200 mm/hr
                unit = "mm/hr"
            elif sensor.sensor_type == "river_flow":
                new_value = max(0, min(1, new_value))  # 0-1 (normalized)
                unit = "ratio"
            elif sensor.sensor_type == "drainage":
                new_value = max(0, min(1, new_value))  # 0-1 (normalized)
                unit = "ratio"
            else:
                unit = "units"
            
            # Update sensor state
            sensor.last_value = new_value
            sensor.last_update = current_time
            
            return {
                "value": round(new_value, 2),
                "unit": unit,
                "timestamp": current_time.isoformat(),
                "quality": random.choice(["good", "fair", "excellent"]),
                "calibration_status": random.choice(["calibrated", "needs_calibration"])
            }
            
        except Exception as e:
            logger.error(f"❌ Generate sensor data error: {str(e)}")
            return {"value": 0, "unit": "error", "timestamp": datetime.now().isoformat()}
    
    async def forward_to_system(self, node_id: str, data: Dict[str, Any], protocol: str):
        """Forward sensor data to main JalRakshā system"""
        try:
            payload = {
                "node_id": node_id,
                "protocol": protocol,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            response = requests.post(self.http_endpoint, json=payload, timeout=5)
            
            if response.status_code == 200:
                logger.info(f"✅ Data forwarded to system for {node_id}")
            else:
                logger.error(f"❌ Failed to forward data for {node_id}: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Forward data error for {node_id}: {str(e)}")

class SensorHealthSimulator:
    """Simulate sensor health and connectivity issues"""
    
    def __init__(self):
        self.health_probabilities = {
            "online": 0.85,    # 85% chance of being online
            "offline": 0.10,  # 10% chance of being offline
            "error": 0.05     # 5% chance of having errors
        }
    
    async def simulate_sensor_health(self, sensor: SensorSimulation) -> Dict[str, Any]:
        """Simulate sensor health status"""
        try:
            # Determine health status based on probabilities
            rand = random.random()
            cumulative = 0
            
            for status, probability in self.health_probabilities.items():
                cumulative += probability
                if rand <= cumulative:
                    health_status = status
                    break
            else:
                health_status = "online"
            
            # Calculate health score
            if health_status == "online":
                health_score = random.randint(80, 100)
            elif health_status == "offline":
                health_score = random.randint(0, 30)
            else:  # error
                health_score = random.randint(30, 70)
            
            # Generate health details
            health_data = {
                "status": health_status,
                "health_score": health_score,
                "last_seen": datetime.now().isoformat(),
                "battery_level": random.uniform(10, 100),
                "signal_strength": random.uniform(-120, -30),
                "error_count": random.randint(0, 10),
                "uptime": random.randint(1000, 86400),
                "temperature": random.uniform(-10, 60),
                "humidity": random.uniform(20, 90)
            }
            
            return health_data
            
        except Exception as e:
            logger.error(f"❌ Health simulation error: {str(e)}")
            return {"status": "error", "health_score": 0}

class EnhancedIoTSimulator:
    """Enhanced IoT Simulator with multiple protocols and health monitoring"""
    
    def __init__(self):
        self.protocol_simulator = IoTProtocolSimulator()
        self.health_simulator = SensorHealthSimulator()
        self.sensors: List[SensorSimulation] = []
        self.simulation_interval = 30  # seconds
        self.database_path = "iot_simulation.db"
        self.init_database()
        
    def init_database(self):
        """Initialize simulation database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_simulation_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT,
                    sensor_type TEXT,
                    protocol TEXT,
                    data_value REAL,
                    health_status TEXT,
                    health_score INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ IoT simulation database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
    
    def create_sensor_network(self):
        """Create comprehensive sensor network across India"""
        try:
            # Water Level Sensors
            water_sensors = [
                SensorSimulation("WL001", "Ganga River Gauge - Patna", "Patna", 25.5941, 85.1376, 
                               "water_level", "mqtt", 3.5, 2.0, 0.5),
                SensorSimulation("WL002", "Yamuna River Gauge - Delhi", "Delhi", 28.7041, 77.1025, 
                               "water_level", "lorawan", 2.8, 1.5, 0.3),
                SensorSimulation("WL003", "Krishna River Gauge - Vijayawada", "Vijayawada", 16.5062, 80.6480, 
                               "water_level", "mqtt", 4.2, 2.5, 0.7),
                SensorSimulation("WL004", "Brahmaputra Gauge - Guwahati", "Guwahati", 26.1445, 91.7362, 
                               "water_level", "lorawan", 5.1, 3.0, 0.8),
                SensorSimulation("WL005", "Godavari Gauge - Rajahmundry", "Rajahmundry", 17.0005, 81.8040, 
                               "water_level", "http", 3.8, 2.2, 0.6),
            ]
            
            # Rainfall Sensors
            rainfall_sensors = [
                SensorSimulation("RF001", "Mumbai Rainfall Station", "Mumbai", 19.0760, 72.8777, 
                               "rainfall", "mqtt", 25.0, 15.0, 5.0),
                SensorSimulation("RF002", "Chennai Rainfall Station", "Chennai", 13.0827, 80.2707, 
                               "rainfall", "lorawan", 30.0, 20.0, 6.0),
                SensorSimulation("RF003", "Kolkata Rainfall Station", "Kolkata", 22.5726, 88.3639, 
                               "rainfall", "mqtt", 35.0, 25.0, 7.0),
                SensorSimulation("RF004", "Bangalore Rainfall Station", "Bangalore", 12.9716, 77.5946, 
                               "rainfall", "http", 20.0, 12.0, 4.0),
                SensorSimulation("RF005", "Hyderabad Rainfall Station", "Hyderabad", 17.3850, 78.4867, 
                               "rainfall", "mqtt", 22.0, 14.0, 4.5),
            ]
            
            # River Flow Sensors
            river_flow_sensors = [
                SensorSimulation("RF006", "Ganga Flow Monitor - Varanasi", "Varanasi", 25.3176, 82.9739, 
                               "river_flow", "lorawan", 0.4, 0.2, 0.1),
                SensorSimulation("RF007", "Yamuna Flow Monitor - Agra", "Agra", 27.1767, 78.0081, 
                               "river_flow", "mqtt", 0.3, 0.15, 0.08),
                SensorSimulation("RF008", "Kaveri Flow Monitor - Mysore", "Mysore", 12.2958, 76.6394, 
                               "river_flow", "http", 0.5, 0.25, 0.12),
            ]
            
            # Drainage Capacity Sensors
            drainage_sensors = [
                SensorSimulation("DC001", "Delhi Drainage Monitor", "Delhi", 28.6139, 77.2090, 
                               "drainage", "mqtt", 0.7, 0.2, -0.1),
                SensorSimulation("DC002", "Bangalore Drainage Monitor", "Bangalore", 12.9716, 77.5946, 
                               "drainage", "lorawan", 0.6, 0.25, -0.15),
                SensorSimulation("DC003", "Mumbai Drainage Monitor", "Mumbai", 19.0760, 72.8777, 
                               "drainage", "mqtt", 0.8, 0.15, -0.05),
            ]
            
            # Combine all sensors
            self.sensors = water_sensors + rainfall_sensors + river_flow_sensors + drainage_sensors
            
            logger.info(f"✅ Created sensor network with {len(self.sensors)} sensors")
            
        except Exception as e:
            logger.error(f"❌ Create sensor network error: {str(e)}")
    
    async def simulate_sensor_data(self, sensor: SensorSimulation):
        """Simulate data transmission for a single sensor"""
        try:
            # Simulate health status
            health_data = await self.health_simulator.simulate_sensor_health(sensor)
            
            # Only transmit data if sensor is online
            if health_data["status"] == "online":
                # Simulate data transmission based on protocol
                if sensor.protocol == "mqtt":
                    transmission_data = await self.protocol_simulator.simulate_mqtt_sensor(sensor)
                elif sensor.protocol == "lorawan":
                    transmission_data = await self.protocol_simulator.simulate_lorawan_sensor(sensor)
                elif sensor.protocol == "http":
                    transmission_data = await self.protocol_simulator.simulate_http_sensor(sensor)
                else:
                    logger.warning(f"⚠️ Unknown protocol for sensor {sensor.node_id}")
                    return
                
                # Log simulation data
                await self.log_simulation_data(sensor, health_data)
                
            else:
                logger.warning(f"⚠️ Sensor {sensor.node_id} is {health_data['status']}")
                
        except Exception as e:
            logger.error(f"❌ Sensor simulation error for {sensor.node_id}: {str(e)}")
    
    async def log_simulation_data(self, sensor: SensorSimulation, health_data: Dict[str, Any]):
        """Log simulation data to database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sensor_simulation_log 
                (node_id, sensor_type, protocol, data_value, health_status, health_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sensor.node_id,
                sensor.sensor_type,
                sensor.protocol,
                sensor.last_value,
                health_data["status"],
                health_data["health_score"]
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Log simulation data error: {str(e)}")
    
    async def run_simulation(self):
        """Run continuous IoT simulation"""
        try:
            logger.info("🌊 Starting Enhanced IoT Simulator...")
            
            # Create sensor network
            self.create_sensor_network()
            
            # Run simulation loop
            while True:
                logger.info(f"🔄 Running simulation cycle for {len(self.sensors)} sensors...")
                
                # Simulate all sensors concurrently
                tasks = [self.simulate_sensor_data(sensor) for sensor in self.sensors]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Wait for next cycle
                await asyncio.sleep(self.simulation_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 IoT Simulator stopped by user")
        except Exception as e:
            logger.error(f"❌ Simulation error: {str(e)}")
    
    async def get_simulation_stats(self) -> Dict[str, Any]:
        """Get simulation statistics"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Get total simulations
            cursor.execute("SELECT COUNT(*) FROM sensor_simulation_log")
            total_simulations = cursor.fetchone()[0]
            
            # Get protocol distribution
            cursor.execute("SELECT protocol, COUNT(*) FROM sensor_simulation_log GROUP BY protocol")
            protocol_stats = dict(cursor.fetchall())
            
            # Get sensor type distribution
            cursor.execute("SELECT sensor_type, COUNT(*) FROM sensor_simulation_log GROUP BY sensor_type")
            sensor_type_stats = dict(cursor.fetchall())
            
            # Get health status distribution
            cursor.execute("SELECT health_status, COUNT(*) FROM sensor_simulation_log GROUP BY health_status")
            health_stats = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "total_simulations": total_simulations,
                "protocol_distribution": protocol_stats,
                "sensor_type_distribution": sensor_type_stats,
                "health_status_distribution": health_stats,
                "active_sensors": len(self.sensors),
                "simulation_interval": self.simulation_interval
            }
            
        except Exception as e:
            logger.error(f"❌ Get simulation stats error: {str(e)}")
            return {}

# Main execution
async def main():
    """Main Enhanced IoT Simulator execution"""
    logger.info("🌊 Starting JalRakshā AI Enhanced IoT Simulator V2...")
    
    simulator = EnhancedIoTSimulator()
    
    # Run simulation
    await simulator.run_simulation()

if __name__ == "__main__":
    asyncio.run(main())

